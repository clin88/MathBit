from builtins import slice
from decimal import Decimal as D
from decimal import DecimalException
from functools import reduce, total_ordering, wraps
from collections import OrderedDict
from numbers import Number
from utils import cat
from zipper import Cursor

# TODO: Don't need fractions anymore, just represent using exponents
# TODO: Write printer functions.
# TODO: Create an 'identity node' in place of using 0's and 1's

def _mathify(arg):
    if isinstance(arg, Base):
        return arg
    elif isinstance(arg, Number):
        return Nmbr(arg)
    elif isinstance(arg, str):
        if '.' in arg:
            return Nmbr(arg)
        else:
            return Symbol(arg)
    else:
        raise TypeError("Not a math object: %s." % arg)

def mathify(piece=slice(0,None,None)):
    """Wrapper to ensure all arguments are mathified. Only necessary on public functions
    that take arbitrary inputs. Only acts on args, not kwargs.

    Slice can be used to specify which arguments to mathify."""

    def _(f):
        """What the hell why didn't they just make the first argument for a decorator function
        the function and not require this double nesting nonsense?
        """

        @wraps(f)
        def __(*args, **kwargs):
            args = list(args)
            mathifyargs = args.__getitem__(piece)
            mathifyargs = list(map(_mathify, mathifyargs))
            args.__setitem__(piece, mathifyargs)

            return f(*args, **kwargs)
        return __
    return _

class Base():
    """Mix in that loads in defaults for operators.
    """

    @staticmethod
    @mathify()
    def _pow(base, power):
        if 1 in [base, power]:
            return base if power == 1 else 1
        else:
            return Exp(base, power)

    def __pow__(self, power, modulo=None):
        return self._pow(self, power)

    def __rpow__(self, power, modulo=None):
        return self._pow(power, self)

    @staticmethod
    @mathify()
    def _mul(a, b):
        isnmbr = lambda n: isinstance(n, Number)
        if 1 in [a, b]:
            return a if b == 1 else b
        elif -1 in [a, b] and all(map(isnmbr, [a,b])):
            return -a if b == -1 else -b
        else:
            return Mult(*cat(a, b, flatten=Mult))

    def __mul__(self, other):
        return self._mul(self, other)

    def __rmul__(self, other):
        return self._mul(other, self)

    @staticmethod
    @mathify()
    def _div(num, denom):
        if denom == 1:
            return num
        else:
            return Frac(num, denom)

    def __truediv__(self, other):
        if other == 0:
            raise ArithmeticError("Division by zero :(. The fabric of space time is at stake here!")
        return self._div(self, other)

    def __rtruediv__(self, other):
        return self._div(other, self)

    @staticmethod
    @mathify()
    def _add(a, b):
        if 0 in [a,b]:
            return a if b == 0 else b
        else:
            return Plus(*cat(a, b, flatten=Plus))

    def __add__(self, other):
        return self._add(self, other)

    def __radd__(self, other):
        return self._add(other, self)

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return other + -self

    def __neg__(self):
        return -1 * self

class Operator(Base, tuple):
    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(cat(self, self.__class__))

    @mathify(piece=slice(1,None,None))
    def __new__(cls, *args):
        return super().__new__(cls, args)

    def __repr__(self):
        r = lambda x, y: str(x) + self.sign + str(y)
        return "(" + str(reduce(r, self)) + ")"

    def __getitem__(self, arg):
        item = super().__getitem__(arg)
        if isinstance(arg, slice):
            try:
                return type(self)(*item)
            except TypeError:
                return tuple(item)
        else:
            return item

    def append(self, *node):
        return self.__class__(*(self + tuple(node)))

    def insert(self, index, *items):
        return self.__class__(*(self[:index] + tuple(items) + self[index + 1:]))

class Commutative(Operator):
    def __hash__(self):
        # returns an order agnostic hash
        sortedhashes = sorted(map(hash, self))
        sortednode = tuple(cat(sortedhashes, self.__class__))
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
        elif isinstance(value, Nmbr):
            self.value = value.value
        else:
            self.value = value

    @property
    def p(self):
        return getattr(self.value, 'numerator', self.value)

    @property
    def q(self):
        return getattr(self.value, 'denominator', Nmbr(1))

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if not isinstance(other, Number):
            return False
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
        return hash(self) == hash(other)

class OpCursor(Cursor):
    def upper(self):
        children = cat(self.left_siblings, (self.node,), self.right_siblings)
        return self.upnode.__class__(*children)

    def replaceyield(self, node):
        if node != self.node:
            self = self.replace(node)
            yield self

        return self