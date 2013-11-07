from base import BaseOperator, Noncommutative


class Brackets(BaseOperator):
    def __repr__(self):
        s = "(%s)"
        return s % super(Brackets, self).__repr__()


class Plus(BaseOperator):
    sign = '+'


class Mult(BaseOperator):
    sign = '*'


class Minus(BaseOperator):
    sign = '-'


class Pow(Noncommutative):
    sign = '^'
    order = Noncommutative.RIGHT_TO_LEFT


class Fraction(Noncommutative):
    sign = '/'
    order = Noncommutative.LEFT_TO_RIGHT


class Eq(BaseOperator):
    sign = '='

