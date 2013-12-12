from numbers import Number
from functools import reduce
from operator import neg, mul, pow, add
from itertools import repeat, filterfalse
from core.ops import Nmbr
from core.zipper import OpCursor
from parse import parse
from core import Exp, Mult, Frac, Plus
from utils import genhelper, identityiter, OrderedDefaultDict, flatten, cat, identity


# TODO: Deal with fractions better.
# TODO: Output formatter.
# TODO: Define simplification more formally to help simplify code and expectations.
# TODO: Adding fractions.
# TODO: Step by step arithmetic evaluation.

@genhelper
def simplify(expression):
    if type(expression) is str:
        expression = parse(expression)

    cursor = OpCursor.makecursor(expression)
    result = yield from simpdispatch(cursor)
    return result.node


@genhelper
def simpdispatch(cursor):
    """Dispatch function.
    """
    dispatch = {
        Plus: simpplus,
        Mult: simpmult,
        Frac: simpfrac,
        Exp: simpexp
    }

    op = type(cursor.node)
    cursor = yield from dispatch.get(op, identityiter)(cursor)

    return cursor


@genhelper
def simpchildren(cursor):
    """Simplifies the children of the focus node. Returns a cursor to the original focus node.
    """
    if not cursor.can_down():
        return cursor

    cursor = cursor.movedown()

    while True:
        cursor = yield from simpdispatch(cursor)
        if cursor.canright():
            cursor = cursor.moveright()
        else:
            break

    cursor = cursor.moveup()
    return cursor


@genhelper
def simpexp(cursor):
    cursor = yield from simpchildren(cursor)

    base = cursor.node.base
    exponent = cursor.node.exponent

    node = None
    if exponent == 1:
        node = cursor.node.base
    elif isinstance(base, Frac):
        node = base.numer ** exponent / base.denom ** exponent
    elif isinstance(base, Exp):
        node = base.base ** (base.exponent * exponent)
    elif isinstance(base, Mult):
        node = reduce(mul, map(pow, base, repeat(exponent)))
    elif isinstance(base, Nmbr) and isinstance(exponent, Nmbr):
        # TODO: Replace with evaluate syntax
        node = base.value ** exponent.value

    if node is not None:
        cursor = yield from cursor.replaceyield(node)
        cursor = yield from simpdispatch(cursor)

    return cursor


@genhelper
def simpmult(cursor):
    """
        Takes the terms in an expression, seperates numerators and denominators, and simplifies the result.

        e.g. 3 * x / 4 * y = 3xy / 4
    """
    cursor = yield from simpchildren(cursor)

    # if there are fractions, combine into one big fraction and delegate to simpfrac

    # TODO: When we have evalexpr, put off constant evaluation until next step.
    constant = 1
    factors = OrderedDefaultDict(lambda: Nmbr(0))

    # flatten any nested mults
    node = flatten(cursor.node)
    cursor = yield from cursor.replaceyield(node)

    # count factors
    for factor in node:
        if isinstance(factor, Nmbr):
            constant *= factor.value
        elif isinstance(factor, Exp):
            factors[factor.base] += factor.exponent
        else:
            factors[factor] += 1

    # reconstruct
    factors = map(pow, factors.keys(), factors.values())
    node = constant * reduce(mul, factors, 1)

    cursor = yield from cursor.replaceyield(node)
    cursor = yield from simpchildren(cursor)

    # if there is a fraction, join into fraction and delegate to simpfrac
    isfrac = lambda obj: isinstance(obj, Frac)
    if any(map(isfrac, cat(cursor.node))):
        getnumer = lambda node: getattr(node, 'numer', node)
        getdenom = lambda node: getattr(node, 'denom', 1)

        # TODO: Simplification of entire line before separating into fractions
        numerator = reduce(mul, map(getnumer, cursor.node))
        denominator = reduce(mul, map(getdenom, cursor.node))

        cursor = yield from cursor.replaceyield(numerator / denominator)
        cursor = yield from simpfrac(cursor)

    return cursor


@genhelper
def simpplus(cursor):
    """
        Plus and Mult: c + c + xy + xy -> 2c + 2xy
        Exponents too: c^2 + c^2 = 2c^2
    """
    cursor = yield from simpchildren(cursor)

    # flatten nested Pluses
    node = flatten(cursor.node)
    cursor = yield from cursor.replaceyield(node)

    # count terms
    terms = OrderedDefaultDict(lambda: Nmbr(0))
    constant = 0
    for term in node:
        if isinstance(term, Nmbr):
            constant += term.value
        elif isinstance(term, Mult):
            # split coefficient, assuming constant factor is first
            coeff, term = (term[0], term[1:]) if isinstance(term[0], Nmbr) else (1, term)
            terms[term] += coeff
        else:
            terms[term] += 1

    terms = map(mul, terms.values(), terms.keys())
    node = reduce(add, terms, 0) + constant

    cursor = yield from cursor.replaceyield(node)
    cursor = yield from simpchildren(cursor)

    return cursor


@genhelper
def simpfrac(cursor):
    """
        n, symb, M, E, P

        n / n -> reduce
        xy / y

    """
    cursor = yield from simpchildren(cursor)

    # deal with compound fractions
    if isinstance(cursor.node.numer, Frac) or isinstance(cursor.node.denom, Frac):
        numer = cursor.node.numer
        denom = cursor.node.denom

        newnum = getattr(numer, 'numer', numer) * getattr(denom, 'denom', 1)
        newdenom = getattr(numer, 'denom', 1) * getattr(denom, 'numer', denom)

        cursor = yield from cursor.replaceyield(newnum / newdenom)

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
    factors = OrderedDefaultDict(lambda: Nmbr(0))
    constant = Nmbr(1)

    # count factors
    for op, node in [(identity, cursor.node.numer), (neg, cursor.node.denom)]:
        for factor in cat(node, flatten=Mult):
            if isinstance(factor, Exp):
                factors[factor.base] += op(factor.exponent)
            elif isinstance(factor, Number):
                constant *= (factor ** op(1))
            else:
                factors[factor] += op(1)

    # reconstruct fraction
    def isdenom(factor):
        exponent = getattr(factor, 'exponent', 1)
        return isinstance(exponent, Number) and exponent < 0

    constant = evalexpr(constant)
    factors = list(map(pow, factors.keys(), factors.values()))

    numer = filterfalse(isdenom, factors)
    numer = constant.p * reduce(mul, numer, 1)

    denom = filter(isdenom, factors)
    denom = map(lambda factor: simplify(factor ** -1).eval(), denom)
    denom = constant.q * reduce(mul, denom, 1)

    cursor = yield from cursor.replaceyield(numer / denom)
    #cursor = yield from simpchildren(cursor)

    return cursor

def evalexpr(expr):
    """Evaluates a numbers only expression tree.

    Mult(5, 4, 3) -> 5 * 4 * 3 = 60
    Plus(1, 2, Mult(3, 4), 5) = 20
    """
    if isinstance(expr, Nmbr):
        return expr

    getval = lambda nmbr: nmbr.value if isinstance(nmbr, Nmbr) else evalexpr(nmbr).value
    vals = list(map(getval, expr))

    if type(expr) == Mult:
        val = reduce(mul, vals, 1)
    elif type(expr) == Frac:
        val = vals[0] / vals[1]
    elif type(expr) == Plus:
        val = reduce(add, vals, 0)
    elif type(expr) == Exp:
        val = vals[0] ** vals[1]

    return Nmbr(val)
