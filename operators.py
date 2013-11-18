from decimal import Decimal as D
from functools import total_ordering
from numbers import Number as N
from base import Node, Operator, Noncommutative, Commutative

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


class Exp(Noncommutative):
    sign = '^'
    oop = 1
    order = Noncommutative.RIGHT_TO_LEFT

    @property
    def base(self):
        return self.children[0]

    @property
    def exponent(self):
        return self.children[1]


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


@total_ordering
class Number(Node):
    def __init__(self, arg):
        if type(arg) is str:
            self.number = D(arg) if '.' in arg else int(arg)
        elif type(arg) is float:
            self.number = D(arg)
        else:
            self.number = arg

        super(Number, self).__init__(arg)

    def __repr__(self):
        return str(self.number)

    def __gt__(self, other):
        if isinstance(other, Number):
            return self.number > other.number
        else:
            return self.number > other

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.number + other.number)
        else:
            return Number(self.number + other)

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.number * other.number)
        else:
            return Number(self.number * other)

    def __rmul__(self, other):
        return self * other

    def __hash__(self):
        return hash(self.number)


@total_ordering
class Symbol(Node):
    def __init__(self, arg):
        self.symbol = arg
        super(Symbol, self).__init__(arg)

    def __repr__(self):
        return self.symbol

    def __gt__(self, other):
        return self.symbol > other

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.symbol)


def mathify(obj):
    if isinstance(obj, N):
        return Number(obj)
    elif isinstance(obj, str):
        return Symbol(obj)
    else:
        raise TypeError("Object %s not a valid math type. Cannot coerce into Number or Symbol." % repr(obj))