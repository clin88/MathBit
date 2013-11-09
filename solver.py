import numbers
from operators import *
from base import BaseOperator


def _simplify_mult(expr):
    index = 0
    constants = []
    while index < len(expr.children):
        child = expr.children[index]

        if isinstance(child, BaseOperator):
            child = simplify_expr(child)

        # remove nested multiplication. e.g. 2 * (x * 3) -> 2 * x * 3
        if isinstance(child, Mult):
            expr.add_children(*child.children)
            expr.pop_child(index)

        elif isinstance(child, Number):
            constants.append(child)
            expr.pop_child(index)

        else:
            index += 1

    constant = reduce(lambda x, y: x * y, constants)
    expr.insert_child(0, constant)

    # if after simplification, node is only one item, carry it out
    if isinstance(expr, BaseOperator) and len(expr.children) == 1:
        expr.replace_child(index, expr.children[0])

def simplify_expr(expr):
    """
        Simplifies an expression. Handles the following cases:

        1. Combines like terms.
    """
    i = 0
    while i < len(expr.children):
        node = expr.children[i]
        if isinstance(node, Mult):
            _simplify_mult(node)

        i += 1
    return expr


# TODO: Use numbers module for numbers.
# TODO: Subclass children list and override inplace change methods for simpler syntax and better safety
