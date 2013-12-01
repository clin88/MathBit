from numbers import Number
from collections import OrderedDict

from ops import Exp, Mult, Fraction, Plus
from zipper import make_cursor


def simplify(expression):
    result = yield from _simplify(make_cursor(expression))
    return result.node


def _simplify(cursor):
    """
        Dispatch function
    """
    node = cursor.node
    if isinstance(node, Plus):
        cursor = yield from _simplify_plus(cursor)
    if isinstance(node, Mult):
        cursor = yield from _simplify_mult(cursor)
        #elif isinstance(node, Fraction):
    #    cursor = yield from _simplify_fraction(cursor)
    #elif isinstance(node, Exp):
    #    cursor = yield from _simplify_exp(cursor)

    return cursor


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


def _simplify_exp(cursor):
    pass


def _simplify_mult(cursor):
    """
        Takes the terms in an expression, seperates numerators and denominators, and simplifies the result.

        e.g. 3 * x / 4 * y = 3xy / 4
    """
    cursor = yield from _simplify_children(cursor)

    numerator = Mult()
    denominator = Mult()

    for child in cursor.node:
        if isinstance(child, Fraction):
            numerator = numerator.append(child.numerator)
            denominator = denominator.append(child.denominator)
        else:
            numerator = numerator.append(child)

    if not denominator:
        cursor = yield from _simplify_product(cursor)
    else:
        cursor = cursor.replace_self(Fraction(numerator, denominator))
        yield cursor

        cursor = yield from _simplify_fraction(cursor)

    return cursor


def _simplify_product(cursor):
    """
        Simplifies a Mult() containing no fractions.
    """
    node = cursor.node
    constant = 1
    index = 0
    factors = OrderedDict()
    while index < len(node):
        child = node[index]
        if isinstance(child, Mult):
            node = node.insert(index, child)
            continue
        elif isinstance(child, Number):
            constant *= child
        elif isinstance(child, Exp):
            factors.setdefault(child.base, []).append(child.exponent)
        else:
            factors.setdefault(child, []).append(1)

        index += 1

    node = Mult()
    if constant != 1:
        node = node.append(constant)
    for factor, power in factors.items():
        node = node.append(Exp(factor, Plus(*power)))

    # if after simplification, node is only one item, carry it out
    if len(node) == 1:
        node = node[0]

    cursor = cursor.replace_self(node)
    yield cursor

    cursor = yield from _simplify_children(cursor)
    return cursor


def _simplify_plus(cursor):
    """
        Plus and Mult: c + c + xy + xy -> 2c + 2xy
        Exponents too: c^2 + c^2 = 2c^2
    """
    cursor = yield from _simplify_children(cursor)

    constant = 0
    terms = OrderedDict()
    node = cursor.node
    index = 0
    while index < len(node):
        child = node[index]
        if isinstance(child, Plus):
            node = child + node[1:]
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
        node = node + (constant,)

    if len(node) == 1:
        node = node[0]

    cursor = cursor.replace_self(node)
    yield cursor

    cursor = yield from _simplify_children(cursor)
    return cursor


#def _simplify_fraction(self, node):
#    self._simplify_expr(node.numerator)
#    self._simplify_expr(node.denominator)
#
#    numerator = node.numerator
#    denominator = node.denominator
#    if isinstance(numerator, Fraction):
#        if isinstance(denominator, Fraction):
#            replacement = Mult(numerator, Fraction(denominator.denominator, denominator.numerator))
#            node.replace_self(replacement)
#            # TODO: report step
#            self._simplify_expr(node)
#
#        else:
#            replacement = Mult(numerator, Fraction(1, denominator))
#            node.replace_self(replacement)
#            self._simplify_expr(node)
#
#    elif isinstance(numerator, Exp):
#        if isinstance(denominator, Exp):
#            if numerator.base == denominator.base:
#                replacement = Exp(numerator.base, numerator.exponent - denominator.exponent)
#        elif isinstance(denominator, Mult):
#            pass
#
#
#    elif isinstance(numerator, Mult):
#        pass

