from decimal import Decimal as D
from base import BaseOperator, Noncommutative, Node
"""
    Order of operations:

        () = 0
        ^ = 1
        */ = 2
        +- = 3
"""

class Expr(BaseOperator):
    oop = 99
    def __repr__(self):
        return repr(self.children[0])

class Pow(Noncommutative):
    sign = '^'
    oop = 1
    order = Noncommutative.RIGHT_TO_LEFT


class Mult(BaseOperator):
    sign = '*'
    oop = 2


class Fraction(Noncommutative):
    sign = '/'
    oop = 2
    order = Noncommutative.LEFT_TO_RIGHT


class Plus(BaseOperator):
    sign = '+'
    oop = 3


class Eq(BaseOperator):
    sign = '='
    oop = 10


class Number(Node):
    def __init__(self, arg):
        if type(arg) is str:
            self.number = D(arg) if '.' in arg else int(arg)
        else:
            self.number = arg

        super(Number, self).__init__(arg)

    def __repr__(self):
        return str(self.number)

    def __eq__(self, other):
        return self.number == other.number

    def __ne__(self, other):
        return not self.__eq__(other)

    def __mul__(self, other):
        return Number(self.number * other.number)


class Symbol(Node):
    def __init__(self, arg):
        self.symbol = arg
        super(Symbol, self).__init__(arg)

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __ne__(self, other):
        return not self.__eq__(other)
