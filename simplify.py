from numbers import Number
from collections import OrderedDict

from parse import parse
from ops import Exp, Mult, Fraction, Plus
from zipper import make_cursor

# used as the hash key in lists of factors to indicate the constant value
constant = hash(Number)


def simplify(expression):
    if type(expression) is str:
        expression = parse(expression)

    cursor = make_cursor(expression)
    result = yield from _simplify(cursor)
    return result.node


def _simplify(cursor):
    """
        Dispatch function
    """
    node = cursor.node
    if isinstance(node, Plus):
        cursor = yield from _simplify_plus(cursor)
    elif isinstance(node, Mult):
        cursor = yield from _simplify_mult(cursor)
    #elif isinstance(node, Fraction):
    #    cursor = yield from _simplify_fraction(cursor)
    elif isinstance(node, Exp):
        cursor = yield from _simplify_exp(cursor)

    return cursor


def _simplify_wrapper(f):
    """
        Decorates simplification functions to ensure that children nodes
        are simplified.
    """

    def simplify_wrapper(cursor):
        cursor = yield from _simplify_children(cursor)
        cursor = yield from f(cursor)
        return cursor

    return simplify_wrapper


def _simplify_children(cursor):
    """
        Simplifies the children of the focus node. Returns a cursor to the original focus node.
    """
    if not cursor.can_down():
        return cursor

    cursor = cursor.down()
    cursor = yield from _simplify(cursor)
    while cursor.can_right():
        cursor = cursor.right()
        cursor = yield from _simplify(cursor)

    cursor = cursor.up()
    return cursor


@_simplify_wrapper
def _simplify_exp(cursor):
    # mult, plus, fraction, exp
    # (x / y) ^ * -> x^* / y^*
    # (x ^ y) ^ z -> x ^ y ^ z
    # (x ^ y) ^ (a ^ b) -> x ^ y ^ (a ^ b)
    # c1 ^ c2 -> eval(c1 ^ c2)

    base = cursor.node.base
    exponent = cursor.node.exponent

    if isinstance(base, Fraction):
        numer = Exp(base.numer, exponent)
        denom = Exp(base.denom, exponent)
        cursor = cursor.replace_self(Fraction(numer, denom))
    elif isinstance(base, Exp):
        new_base = base.base
        new_exponent = Mult(base.exponent, exponent)
        cursor = cursor.replace_self(Exp(new_base, new_exponent))
    elif isinstance(base, Mult):
        node = Mult()
        for factor in base:
            node = node.append(Exp(factor, exponent))
        cursor = cursor.replace_self(node)
    elif isinstance(base, Number) and isinstance(exponent, Number):
        node = base ** exponent
        cursor = cursor.replace_self(node)

    yield cursor

    node = cursor.node
    if isinstance(node, Exp) and node.exponent == 1:
        cursor = cursor.replace_self(cursor.node.base)
        yield cursor

    cursor = yield from _simplify_children(cursor)

    return cursor


@_simplify_wrapper
def _simplify_mult(cursor):
    """
        Takes the terms in an expression, seperates numerators and denominators, and simplifies the result.

        e.g. 3 * x / 4 * y = 3xy / 4
    """
    numerator = Mult()
    denominator = Mult()

    for child in cursor.node:
        if isinstance(child, Fraction):
            numerator = numerator.append(child.numer)
            denominator = denominator.append(child.denom)
        else:
            numerator = numerator.append(child)

    if not denominator:
        cursor = yield from _simplify_product(cursor)
    else:
        cursor = cursor.replace_self(Fraction(numerator, denominator))
        yield cursor

    return cursor


def _simplify_product(cursor):
    """
        Simplifies a Mult() containing no fractions.
    """
    constant, factors = _count_factors(cursor.node)

    # rewrite, combining factors
    node = Mult()
    if constant != 1:
        node = node.append(factors[constant])

    for factor, power in factors.items():
        if power == [1]:
            node = node.append(factor)
        else:
            node = node.append(Exp(factor, Plus(*power)))

    # if after simplification, node is only one item, carry it out
    if len(node) == 1:
        node = node[0]

    cursor = cursor.replace_self(node)
    yield cursor

    cursor = yield from _simplify_children(cursor)
    return cursor


@_simplify_wrapper
def _simplify_plus(cursor):
    """
        Plus and Mult: c + c + xy + xy -> 2c + 2xy
        Exponents too: c^2 + c^2 = 2c^2
    """
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

    cursor = cursor.replace_self(node)
    yield cursor

    return cursor


@_simplify_wrapper
def _simplify_fraction(cursor):
    """
        n, symb, M, E, P

        n / n -> reduce
        xy / y

    """

    numer = cursor.node.numer
    denom = cursor.node.denom
    is_frac = lambda n: isinstance(n, Fraction)

    # deal with compound fractions
    while True:
        if is_frac(numer) and is_frac(denom):
            numer = Mult(numer.numer, denom.denom)
            denom = Mult(numer.denom, denom.numer)
        elif is_frac(numer) and not is_frac(denom):
            numer = numer.numer
            denom = Mult(numer.denom, denom)
        elif not is_frac(numer) and is_frac(denom):
            numer = Mult(numer, denom.denom)
            denom = denom.numer
        else:
            break

    cursor = cursor.replace_self(Fraction(numer, denom))
    yield cursor

    # eliminate like factors on top and bottom
    list_factors = lambda x: x if isinstance(x, Mult) else (x,)
    numer_factors = list_factors(numer)
    denom_factors = list_factors(denom)
    intersection = [dfact for nfact in numer_factors
                    for dfact in denom_factors if nfact == dfact]

    if intersection:
        numer_factors = [f for f in numer_factors if f not in intersection]
        denom_factors = [f for f in denom_factors if f not in intersection]
        replacement = Mult(
            Fraction(Mult(intersection), Mult(intersection)),
            Fraction(numer_factors, denom_factors)
        )
        cursor = cursor.replace_self(replacement)
        yield cursor

        replacement = Fraction(numer_factors, denom_factors)
        cursor = cursor.replace_self(replacement)
        yield cursor

    # count factors
    numer_factors = _count_factors(cursor.node.numer)
    denom_factors = _count_factors(cursor.node.denom)
    for factor in numer_factors:
        if factor in denom_factors:
            numer_factors[factor] = [numer_factors.append]


def _count_factors(node):
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
        node.setdefault(node.base, []).append(node.exponent)
    elif isinstance(node, Number):
        constant *= node
    else:
        factors.setdefault(node, []).append(1)

    return constant, factors