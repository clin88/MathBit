from functools import reduce
#Order of operations:
#
#    () = 0
#    ^ = 1
#    */ = 2
#    +- = 3

class Operator(tuple):
    def __repr__(self):
        r = lambda x, y: str(x) + self.sign + str(y)
        return "(" + reduce(r, self) + ")"

class Commutative(Operator):
    def __new__(cls, *args):
        return super().__new__(cls, args)

    def __hash__(self):
        return hash(tuple(sorted(self)))

class Exp(Operator):
    sign = '^'
    oop = 1

    def __new__(cls, *args):
        if len(args) > 2:
            args = (args[0], cls(*args[1:]))

        return super().__new__(cls, args)

    @property
    def base(self):
        return self[0]

    @property
    def exponent(self):
        return self[1]


class Mult(Commutative):
    sign = '*'
    oop = 2


class Fraction(Operator):
    sign = '/'
    oop = 2

    def __new__(cls, *args):
        if len(args) > 2:
            args = (cls(*args[:-1]), args[-1])

        return super().__new__(cls, args)

    @property
    def numerator(self):
        return self[0]

    @property
    def denominator(self):
        return self[1]


class Plus(Commutative):
    sign = '+'
    oop = 3


class Eq(Commutative):
    sign = '='
    oop = 10

