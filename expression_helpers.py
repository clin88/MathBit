from base import BaseOperator
from operators import *

def walk_expr(expr, *types):
    """
        Generator for iterating through all objects of type in *types.
    """
    for child in expr.children:
        # yield this node if no type specified OR this type is in *types
        if not types or type(child) in types:
            yield child

        if isinstance(child, BaseOperator):
            for obj in walk_expr(child, *types):
                yield obj


def mathify(obj):
    if isinstance(obj, D) or isinstance(obj, int) or isinstance(obj, float):
        return Number(obj)
    elif isinstance(obj, str):
        return Symbol(obj)
    else:
        return TypeError("Object %s not a valid math type. Cannot coerce into Number or Symbol." % repr(obj))

