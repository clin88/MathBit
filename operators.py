from base import Operator, Noncommutative, Commutative

"""
    Order of operations:

        () = 0
        ^ = 1
        */ = 2
        +- = 3
"""

class Expr(Operator):
    oop = 99
    def __repr__(self):
        return repr(self.children[0])

class Pow(Noncommutative):
    sign = '^'
    oop = 1
    order = Noncommutative.RIGHT_TO_LEFT


class Mult(Commutative):
    sign = '*'
    oop = 2


class Fraction(Noncommutative):
    sign = '/'
    oop = 2
    order = Noncommutative.LEFT_TO_RIGHT

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

