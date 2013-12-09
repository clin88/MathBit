from numbers import Number
from collections import OrderedDict, defaultdict
from functools import wraps, reduce, partial
from operator import pos, neg, add, mul, imul, pow
from itertools import repeat

from collections.abc import Iterable
from parse import parse
from ops import Exp, Mult, Frac, Plus, Nmbr, OpCursor
from utils import genhelper, identityiter, cat, OrderedDefaultDict


# TODO: Define simplification more formally to help simplify code and expectations.
# TODO: Fractions unnecessary after simplification.
@genhelper
def simplify(expression):
    if type(expression) is str:
        expression = parse(expression)

    cursor = OpCursor.makecursor(expression)
    result = yield from _simplify(cursor)
    return result.node

@genhelper
def _simplify(cursor):
    """Dispatch function.
    """
    dispatch = {
        Plus: _simplify_plus,
        Mult: simpmult,
        Frac: simpfrac,
        Exp: simpexp
    }
    op = type(cursor.node)

    cursor = yield from dispatch.get(op, identityiter)(cursor)
    return cursor

def _ensure_simplified_children(f):
    """
        Decorates simplification functions to ensure that children nodes
        are simplified.
    """

    @wraps(f)
    def __(cursor):
        cursor = yield from _simplify_children(cursor)
        cursor = yield from f(cursor)
        return cursor

    return __


@genhelper
def _simplify_children(cursor):
    """Simplifies the children of the focus node. Returns a cursor to the original focus node.
    """
    if not cursor.can_down():
        return cursor

    cursor = cursor.movedown()

    while True:
        cursor = yield from _simplify(cursor)
        if cursor.canright():
            cursor = cursor.moveright()
        else:
            break

    cursor = cursor.moveup()
    return cursor


@genhelper
@_ensure_simplified_children
def simpexp(cursor):
    # mult, plus, fraction, exp
    # (x / y) ^ * -> x^* / y^*
    # (x ^ y) ^ z -> x ^ y ^ z
    # (x ^ y) ^ (a ^ b) -> x ^ y ^ (a ^ b)
    # c1 ^ c2 -> eval(c1 ^ c2)

    base = cursor.node.base
    exponent = cursor.node.exponent

    if exponent == 1:
        cursor = yield from cursor.replaceyield(cursor.node.base)
    elif isinstance(base, Frac):
        node = base.numer ** exponent / base.denom ** exponent
        cursor = yield from cursor.replaceyield(node)
    elif isinstance(base, Exp):
        node = base.base ** (base.exponent * exponent)
        cursor = yield from cursor.replaceyield(node)
    elif isinstance(base, Mult):
        node = reduce(mul, map(pow, base, repeat(exponent)))
        cursor = yield from cursor.replaceyield(node)
    elif isinstance(base, Number) and isinstance(exponent, Number):
        node = base ** exponent
        cursor = yield from cursor.replaceyield(node)

    cursor = yield from _simplify_children(cursor)

    return cursor


@genhelper
@_ensure_simplified_children
def simpmult(cursor):
    """
        Takes the terms in an expression, seperates numerators and denominators, and simplifies the result.

        e.g. 3 * x / 4 * y = 3xy / 4
    """
    getnumer = lambda node: getattr(node, 'numer', node)
    getdenom = lambda node: getattr(node, 'denom', 1)

    numerator = reduce(mul, map(getnumer, cursor.node))
    denominator = reduce(mul, map(getdenom, cursor.node))

    if denominator != 1:
        # we're actually dealing with a fraction, so delegate there.
        cursor = yield from cursor.replaceyield(numerator / denominator)
        cursor = yield from simpfrac(cursor)
    else:
        # TODO: When we have eval, put off constant evaluation until next step.
        constant = 1
        factors = OrderedDefaultDict(lambda: Nmbr(0))

        # flatten any nested mults
        node = cat(*cursor.node, flatten=Mult)
        cursor = yield from cursor.replaceyield(node)

        for child in node:
            if isinstance(child, Nmbr):
                constant *= child.value
            elif isinstance(child, Exp):
                factors[child.base] += child.exponent
            else:
                factors[child] += 1

        # reconstruct
        factors = map(pow, factors.keys(), factors.values())
        node = Nmbr(constant) * reduce(mul, factors, Nmbr(1))
        cursor = yield from cursor.replaceyield(node)
        cursor = yield from _simplify_children(cursor)

    return cursor


@genhelper
@_ensure_simplified_children
def _simplify_plus(cursor):
    """
        Plus and Mult: c + c + xy + xy -> 2c + 2xy
        Exponents too: c^2 + c^2 = 2c^2
    """
    # count terms
    terms = OrderedDefaultDict(lambda:Nmbr(0))

    node = cat(*cursor.node, flatten=Plus)
    for child in node:
        pass

    constant = 0
    terms = OrderedDict()
    node = cursor.node
    index = 0

    while index < len(node):
        child = node[index]
        if isinstance(child, Plus):
            node = node.insert(index, *child)
        elif isinstance(child, Number):
            constant += child
        elif isinstance(child, Mult):
            # we assume that this is in simplified form, so the constant factor comes first or not at all
            if isinstance(child[0], Number):
                n = child[0]
                terms[child[1:]] = terms.get(child, 0) + n
            else:
                terms[child] = terms.get(child, 0) + 1
        # TODO: Support fractions
        else:
            terms[child] = terms.get(child, 0) + 1

        index += 1

    node = Plus()
    for term, count in terms.items():
        node = node.append(Mult(count, term))
    if constant:
        node = node.append(constant)
    if len(node) == 1:
        node = node[0]

    cursor = yield from replace(cursor, node)

    return cursor


@genhelper
@_ensure_simplified_children
def simpfrac(cursor):
    """
        n, symb, M, E, P

        n / n -> reduce
        xy / y

    """
    # deal with compound fractions
    if isinstance(cursor.node.numer, Frac) or isinstance(cursor.node.denom, Frac):
        cursor = yield from _simplify_compound_fractions(cursor)

    # eliminate like factors on top and bottom
    #list_factors = lambda x: set(x) if isinstance(x, Mult) else {x}
    #numer = set(list_factors(cursor.node.numer))
    #denom = set(list_factors(cursor.node.denom))
    #intersection = numer & denom
    #if intersection:
    #    numer = numer - intersection
    #    denom = denom - intersection
    #    node = Mult(
    #        Frac(Mult(intersection), Mult(intersection)),
    #        Frac(numer, denom)
    #    )
    #    cursor = yield from replace(cursor, node)
    #
    #    node = Frac(numer, denom)
    #    cursor = yield from replace(cursor, node)

    # count factors and its exponents
    factors = {}
    constant = 1
    for node, op in ((cursor.node.numer, pos), (cursor.node.denom, neg)):
        if not isinstance(node, Iterable):
            node = (node,)

        for factor in node:
            if isinstance(factor, Exp):
                factors.setdefault(factor.base, []).append(op(factor.exponent))
            elif isinstance(factor, Number):
                constant *= factor ** op(1)
            else:
                factors.setdefault(factor, []).append(1)

    numer = Nmbr(1)
    denom = Nmbr(1)
    for factor, exponent in factors.items():
        #exponent = reduce(add, exponent)
        exponent = Plus(*exponent)
        if len(exponent) == 1:
            exponent = exponent[0]

        if isinstance(exponent, Number) and exponent < 0:
            denom = denom.append(Exp(factor, exponent))
        else:
            numer = numer.append(Exp(factor, exponent))

    cursor = yield from replace(cursor, Frac(numer,denom))
    cursor = yield from _simplify_children(cursor)

    return cursor

def _simplify_compound_fractions(cursor):
    numer = cursor.node.numer
    denom = reciprocal(cursor.node.denom)
    node = Frac(
        Mult(getattr(numer, 'numer', numer), getattr(denom, 'denom', None)),
        Mult(getattr(numer, 'denom', None), getattr(denom, 'numer', denom))
    )

    cursor = yield from replace(cursor, node)
    return cursor

def _count_factors(node):
    """
    Finds the powers of each factor in node and returns an OrderedDict with key 'factor' and lists of exponent nodes.
    """
    factors = OrderedDict()
    constant = 1
    if isinstance(node, Mult):
        index = 0
        while index < len(node):
            factor = node[index]
            if isinstance(factor, Mult):
                node = node.insert(index, *factor)
                continue
            elif isinstance(factor, Number):
                constant *= factor
            elif isinstance(factor, Exp):
                factors.setdefault(factor.base, []).append(factor.exponent)
            else:
                factors.setdefault(factor, []).append(1)

            index += 1
    elif isinstance(node, Exp):
        factors.setdefault(node.base, []).append(node.exponent)
    elif isinstance(node, Number):
        constant *= node
    else:
        factors.setdefault(node, []).append(1)

    return constant, factors


def reciprocal(node):
    if isinstance(node, Frac):
        return Frac(node.denom, node.numer)
    else:
        return Frac(1, node)
