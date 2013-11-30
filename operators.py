#Order of operations:
#
#    () = 0
#    ^ = 1
#    */ = 2
#    +- = 3

class Commutative(tuple):
    def __new__(cls, *args, ):
        if len(args) > 2:
            args = (args[0], cls(*args[1:]))

        return super().__new__(cls, *args)

class Noncommutative(tuple):
    def __hash__(self):
        return hash(tuple(sorted(self)))

class Exp(Noncommutative):
    sign = '^'
    oop = 1
    order = Noncommutative.RIGHT_TO_LEFT

    def __new__(cls, *args):
        if len(args) > 2:
            args = (args[0], cls(*args[1:]))

        return super().__new__(cls, *args)

    @property
    def base(self):
        return self[0]

    @property
    def exponent(self):
        return self[1]


class Mult(Commutative):
    sign = '*'
    oop = 2


class Fraction(Noncommutative):
    sign = '/'
    oop = 2

    def __new__(cls, *args):
        if len(args) > 2:
            args = (args[0], cls(*args[1:]))

        return super().__new__(cls, *args)

    @property
    def numerator(self):
        return self.children[0]

    @property
    def denominator(self):
        return self.children[1]


class Plus(Commutative):
    sign = '+'
    oop = 3


class Eq(Commutative):
    sign = '='
    oop = 10

