from base import BaseOperator, Noncommutative


class Brackets(BaseOperator):
    def __repr__(self):
        s = "(%s)"
        return s % super(Brackets, self).__repr__()


class Plus(BaseOperator):
    sign = '+'


class Mult(BaseOperator):
    sign = '*'
    # TODO: This is kind of hackish and messy: Should probably find a better way to do this (metaclass?)
    def __new__(cls, *args, **kwargs):
        if args[0] == -1 and len(args) == 2:
            n = args[0] * args[1]
            return n
        else:
            return super(Mult, cls).__new__(cls)

    def __init__(self, *args):
        # assume -1 means that this has been converted from -n to -1 * n.
        # in this case, we want to change this back for presentation purposes.
        args = list(args)
        if args[0] == -1:
            del args[0]
            args[0] *= -1

        super(Mult, self).__init__(*args)


class Pow(Noncommutative):
    sign = '^'
    order = Noncommutative.RIGHT_TO_LEFT


class Minus(BaseOperator):
    sign = '-'


class Fraction(Noncommutative):
    sign = '/'
    order = Noncommutative.LEFT_TO_RIGHT


class Eq(BaseOperator):
    sign = '='
