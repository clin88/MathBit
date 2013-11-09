def mathify(obj):
    if isinstance(obj, D) or isinstance(obj, int) or isinstance(obj, float):
        return Number(obj)
    elif isinstance(obj, str):
        return Symbol(obj)
    else:
        return TypeError("Object %s not a valid math type. Cannot coerce into Number or Symbol." % repr(obj))

