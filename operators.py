from base import BaseOperator, Noncommutative

"""
    Order of operations:

        () = 0
        ^ = 1
        */ = 2
        +- = 3
"""


class Brackets(BaseOperator):
    oop = '0'

    def __repr__(self):
        s = "(%s)"
        return s % super(Brackets, self).__repr__()


class Pow(Noncommutative):
    sign = '^'
    oop = '1'
    order = Noncommutative.RIGHT_TO_LEFT


class Mult(BaseOperator):
    sign = '*'
    oop = '2'


class Fraction(Noncommutative):
    sign = '/'
    oop = '2'
    order = Noncommutative.LEFT_TO_RIGHT


class Plus(BaseOperator):
    sign = '+'
    oop = '3'


class Eq(BaseOperator):
    sign = '='

