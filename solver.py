from collections import OrderedDict
from operators import *
from operators import Number, Operator


def simplify_expr(expr):
    """
        Simplifies an expression. Handles the following cases:

        1. Combines like terms.
    """
    if isinstance(expr, Mult):
        expr = _simplify_mult(expr)
    elif isinstance(expr, Plus):
        expr = _simplify_addition(expr)

    return expr


def _simplify_mult(node):
    """
        Takes the terms in an expression, seperates numerators and denominators, and simplifies the result.

        e.g. 3 * x / 4 * y = 3xy / 4
    """
    numerator = Mult()
    denominator = Mult()

    for child in node.children:
        if isinstance(child, Operator):
            child = simplify_expr(child)

        if isinstance(child, Fraction):
            numerator.add_children(child.numerator)
            denominator.add_children(child.denominator)
        else:
            numerator.add_children(child)

    numerator = _simplify_product(numerator)
    denominator = _simplify_product(denominator)

    # If denominator == 1, return just the numerator. Else return fraction.
    if denominator == 1:
        return numerator
    else:
        # TODO: Simplify this fraction
        return Fraction(numerator, denominator)


def _simplify_product(node):
    """
        Simplifies a Mult() containing no fractions.
    """
    factors = OrderedDict()
    constant = 1
    # iterate through children recording the number of times each factor appears
    while node.children:
        child = node.pop_child(0)

        # remove nested multiplication. e.g. 2 * (x * 3) -> 2 * x * 3
        if isinstance(child, Mult):
            node.insert_child(0, *child.children)
        elif isinstance(child, Number):
            constant *= child
        elif isinstance(child, Exp):
            factors[child.base] = factors.get(child.base, 0) + child.exponent
        else:
            factors[child] = factors.get(child, 0) + 1

    # reconstruct the product, grouping like factors using powers
    if constant != 1:
        node.insert_child(0, constant)
    for factor, power in factors.iteritems():
        node.add_children(Exp(factor,
                              power))                       # TODO: Simplify on the fly, this should also simplify exponents of 1

    # if after simplification, node is only one item, carry it out
    if len(node.children) == 1:
        node = node.children[0]

    return node


def _simplify_addition(node):
    """
        Plus and Mult: c + c + xy + xy -> 2c + 2xy
        Exponents too: c^2 + c^2 = 2c^2
    """
    constant = 0
    terms = OrderedDict()
    while node.children:
        child = node.pop_child(0)
        child = simplify_expr(child)

        if isinstance(child, Plus):
            node.add_children(*child.children)
        elif isinstance(child, Number):
            constant += child
        elif isinstance(child, Mult):
            # we assume that this is in simplified form, so the constant factor comes first or not at all
            if isinstance(child.children[0], Number):
                n = child.pop_child(0)
                terms[child] = terms.get(child, 0) + n
            else:
                terms[child] = terms.get(child, 0) + 1
        # TODO: Support fractions
        else:
            terms[child] = terms.get(child, 0) + 1

    for term, count in terms.iteritems():
        node.add_children(simplify_expr(Mult(count, term)))

    node.add_children(constant)

    if len(node.children) == 1:
        node = node.children[0]

    return node


# TODO: Use numbers module for numbers.
# TODO: Subclass children list and override inplace change methods for simpler syntax and better safety
