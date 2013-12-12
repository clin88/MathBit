from decimal import Decimal as D
from fractions import Fraction
from functools import total_ordering
from numbers import Number
from core.ops import Base


class Symbol(Base):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return hash(self) == hash(other)


@total_ordering
class Nmbr(Base, Number):
    """Wrapper around various Number types. When operations are conducted on Nmbr, it
    returns representations of that operation but does not evaluate the representation.

    To evaluate numbers, access the underlying value attribute, which is always a Decimal.

    To get a fractional representation, access the numerator/denominator properties.
    Or use p and q for short.
    """
    def __repr__(self):
        if self.value % 1 == 0:
            return str(int(self.value))
        else:
            return str(self.value)

    def __init__(self, value):
        if isinstance(value, float):
            # hackish, but don't know enough about binary floats to worry right now
            self.value = D(repr(value))
        elif isinstance(value, Nmbr):
            self.value = value.value
        else:
            self.value = D(value)

    def _asfrac(self):
        return Fraction(self.value)

    @property
    def numerator(self):
        return Nmbr(self._asfrac().numerator)

    @property
    def p(self):
        return self.numerator()

    @property
    def denominator(self):
        return Nmbr(self._asfrac().denominator)

    @property
    def q(self):
        return self.denominator()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, Nmbr):
            return self.value == other.value
        else:
            return self.value == other

    def __lt__(self, other):
        if isinstance(other, Nmbr):
            return self.value < other.value
        else:
            return self.value < other

    def __neg__(self):
        return Nmbr(-self.value)

