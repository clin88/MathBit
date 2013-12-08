from decimal import Decimal as D
from decimal import Decimal, DecimalException
from functools import reduce
from collections import OrderedDict
from numbers import Number
#Order of operations:
#
#    ^ = 1
#    */ = 2
#    +- = 3
from utils import fin


class Operator(tuple):
    def __new__(cls, *args, **kwargs):
        # filter out Nones
        args = [arg for arg in args if arg is not None]

        # if arg has len 1, extract it
        for index, arg in enumerate(args):
            if isinstance(arg, tuple) and len(arg) == 1:
                args[index] = arg[0]
            else:
                pass

        return super().__new__(cls, args)

    def __repr__(self):
        r = lambda x, y: str(x) + self.sign + str(y)
        return "(" + str(reduce(r, self)) + ")"

    def append(self, *node):
        return self.__class__(*(self + tuple(node)))

    def insert(self, index, *items):
        return self.__class__(*(self[:index] + tuple(items) + self[index + 1:]))

    def __hash__(self):
        return hash(self + (self.__class__,))

    def __pow__(self, power, modulo=None):
        return Exp(self, power)

    def __rpow__(self, base, modulo=None):
        return Exp(base, self)

    def __mul__(self, other):
        return Mult(self, other)

    def __rmul__(self, other):
        return Mult(other, self)

class Commutative(Operator):
    def __new__(cls, *args):
        return super().__new__(cls, *args)

    def __hash__(self):
        return hash(sorted(self) + (self.__class__,))

class Exp(Operator):
    sign = '^'
    oop = 1

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

    def count_factors(self):
        # TODO: Finish this function and use it to simplify 'simplify' code
        node = self
        index = 0
        constant = 1
        factors = OrderedDict()

        while index < len(node):
            child = node[index]
            if isinstance(child, Mult):
                node = node.insert(index, child)
                continue
            elif isinstance(child, Number):
                constant *= child
            elif isinstance(child, Exp):
                factors.setdefault(child.base, []).append(child.exponent)
            else:
                factors.setdefault(child, []).append(1)

            index += 1

        return constant, factors

class Frac(Operator):
    sign = '/'
    oop = 2

    def __new__(cls, *args):
        if len(args) > 2:
            args = (cls(*args[:-1]), args[-1])

        return super().__new__(cls, *args)

    @property
    def numer(self):
        return self[0]

    @property
    def denom(self):
        return self[1]


class Plus(Commutative):
    sign = '+'
    oop = 3
    def __neg__(self):
        node = Plus()
        for term in self:
            node = node.append(Mult(-1, term))
        return node

    def __sub__(self, other):
        return Plus(self + -other)

    def __rsub__(self, other):
        return Plus(other + -self)


class Eq(Commutative):
    sign = '='
    oop = 10


class Nmbr(Number):
    def __init__(self, value):
        if isinstance(value, float):
            self.value = D(value)
        elif isinstance(value, str):
            try:
                self.value = D(value)
            except DecimalException:
                raise TypeError("Attempted to parse %s as decimal. Failed." % value)
        else:
            raise TypeError("Only numbers allowed as Nmbr objects.")

    def __mul__(self, other):
        if self.value == 1:
            return other
        elif self.value == 0:
            return Nmbr(0)
        else:
            return Mult(self.value, other)

    def __rdiv__(self, other):
        if self.value == 1:
            return other
        elif self.value == 0:
            raise ZeroDivisionError("What are you doing?! The fabric of space-time is at stake.")
        else:
            return Frac(self, other)

class Symbol(object):
    def __init__(self, name):
        self.name = name
