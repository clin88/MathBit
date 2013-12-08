from decimal import Decimal as D
from decimal import DecimalException
from itertools import chain
from functools import reduce, total_ordering
from collections import OrderedDict
from collections.abc import Iterable
from numbers import Number
from utils import cat
from zipper import Cursor

def flattenif(*iters, type=Iterable):
    """Flattens iters if instance of type.
    """
    unpackif = lambda iter: iter if isinstance(iter, type) else (iter,)
    unpacked = map(unpackif, iters)
    return tuple(chain(*unpacked))

class Base(object):
    """Mix in that loads in defaults for operators.
    """

    def __pow__(self, power, modulo=None):
        return Exp(self, power)

    def __mul__(self, other):
        return Mult(*flattenif(self, other, type=Mult))

    def __truediv__(self, other):
        return Frac(self, other)

    def __add__(self, other):
        return Plus(*flattenif(self, other, type=Plus))

    def __sub__(self, other):
        return Plus(*flattenif(self, -other, type=Plus))

    def __neg__(self):
        return Mult(*flattenif(-1, self, type=Mult))

class Operator(Base, tuple):
    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(flattenif(self, self.__class__))

    def __new__(cls, *args):
        def coerce(v):
            if isinstance(v, Number):
                return Nmbr(v)
            elif isinstance(v, str):
                if '.' in v:
                    return Nmbr(v)
                else:
                    return Symbol(v)
            else:
                return v

        return super().__new__(cls, map(coerce, args))

    def __repr__(self):
        r = lambda x, y: str(x) + self.sign + str(y)
        return "(" + str(reduce(r, self)) + ")"

    def append(self, *node):
        return self.__class__(*(self + tuple(node)))

    def insert(self, index, *items):
        return self.__class__(*(self[:index] + tuple(items) + self[index + 1:]))

class Commutative(Operator):
    def __hash__(self):
        # returns an order agnostic hash
        sortedhashes = sorted(map(hash, self))
        sortednode = tuple(flattenif(sortedhashes, self.__class__))
        return hash(sortednode)

class Exp(Operator):
    sign = '^'
    oop = 1

    def __new__(cls, base, exponent):
        return super().__new__(cls, base, exponent)

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

    def __new__(cls, numer, denom):
        return super().__new__(cls, numer, denom)

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

class Eq(Commutative):
    sign = '='
    oop = 10

@total_ordering
class Nmbr(Base, Number):
    def __repr__(self):
        return str(self.value)

    def __init__(self, value):
        if isinstance(value, float):
            self.value = D(value)
        elif isinstance(value, str):
            try:
                self.value = D(value)
            except DecimalException:
                raise TypeError("Attempted to parse %s as decimal. Failed." % value)
        else:
            self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if not isinstance(other, Number):
            raise TypeError("Comparison between Nmbrs and %s (%s) not supported" % (type(other), other))
        else:
            return self.value == other

    def __lt__(self, other):
        return self.value < other

    def __neg__(self):
        return Nmbr(-self.value)

class Symbol(Base):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        # TODO: Which is best?
        return hash(self) == hash(other)

class OpCursor(Cursor):
    def upper(self):
        children = cat(self.left_siblings, self.node, self.right_siblings)
        return self.upnode.__class__(*children)