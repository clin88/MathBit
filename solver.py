from operators import *
from base import Operator

def simplify_expr(expr):
    """
        Simplifies an expression. Handles the following cases:

        1. Combines like terms.
    """
    node = expr.children[0]
    if isinstance(node, Mult):
        expr.replace_child(0, _simplify_mult(node))

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
    index = 0
    constants = []
    while index < len(node.children):
        child = node.children[index]

        # remove nested multiplication. e.g. 2 * (x * 3) -> 2 * x * 3
        if isinstance(child, Mult):
            node.pop_child(index)
            node.insert_child(index, *child.children)

        elif isinstance(child, Number):
            constants.append(child)
            node.pop_child(index)

        else:
            index += 1

    constant = reduce(lambda x, y: x * y, constants) if constants else Number(1)
    if constant != Number(1):
        node.insert_child(0, constant)

    # if after simplification, node is only one item, carry it out
    if len(node.children) == 1:
        node = node.children[0]
    elif not node.children:
        node = Number(1)

    return node



# TODO: Use numbers module for numbers.
# TODO: Subclass children list and override inplace change methods for simpler syntax and better safety
