def walk_expr(expr, *types):
    """
        Generator for iterating through all objects of type in *types.
    """
    for child in expr.children:
        # yield this node if no type specified OR this type is in *types
        if not types or type(child) in types:
            yield child

        if isinstance(child, Operator):
            for obj in walk_expr(child, *types):
                yield obj




