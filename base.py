"""
Definitions for low level, base operator classes.
"""
from decimal import Decimal as D
from functools import total_ordering
import copy

class Node(object):
    def __init__(self, *args, **kwargs):
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, arg):
        self._parent = arg


@total_ordering
class Operator(Node):
    sign = '?'
    oop = 999

    def __init__(self, *args):
        self._children = []
        self.add_children(*list(args))
        super(Operator, self).__init__(*args)

    def __repr__(self):
        # when parent has operator precedence, show parenthesis to indicate priority:
        #   e.g. Mult(Plus(4, 5), 3): 4 + 5 * 3 -> (4 + 5) * 3

        sign = "%s %s %s"
        if len(self.children) > 1:
            rep = reduce(lambda x, y: sign % (str(x), self.sign, str(y)), self.children)
        else:
            rep = str(self.children[0]) if self.children else repr(None)

        if self.parent and self.parent.oop <= self.oop:
            return '(%s)' % rep
        else:
            return rep

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __gt__(self, other):
        return hash(self) > hash(other)

    def __hash__(self):
        sorted_children = tuple(sorted(self.children))
        return hash(sorted_children)

    @property
    def children(self):
        """
            Note that while children returns a pointer to a mutable list, making changes should be done through the
            helper functions.
        """
        return self._children

    def add_children(self, *args):
        """
            Canonical function for appending to children list.

            Sets _parent property.
        """
        # import must be here to avoid circular reference
        from expression_helpers import mathify

        for arg in args:
            if not isinstance(arg, Node):
                arg = mathify(arg)

            arg.parent = self
            self._children.append(arg)

    def replace_child(self, index, child):
        self._children[index] = child
        child.parent = self

    def pop_child(self, index):
        self._children.pop(index)

    def insert_child(self, index, *children):
        for delta, child in enumerate(children):
            self._children.insert(index + delta, child)
            child.parent = self


class Commutative(Operator):
    pass

class Noncommutative(Operator):
    """
    Describes noncommutative operators. These should be parsed (using division as an example):

    leftright means (1, 2, 3) -> ((1, 2), 3)
    e.g. division: 1 / 2 / 3 == (1 / 2) / 3

    rightleft means (1, 2, 3) -> (1, (2, 3))
    e.g. exponents: 1 ^ 2 ^ 3 == 1 ^ (2 ^ 3)
    """
    LEFT_TO_RIGHT = 'leftright'
    RIGHT_TO_LEFT = 'rightleft'

    def __init__(self, *args):
        if len(args) > 2:
            if self.order == self.LEFT_TO_RIGHT:
                args = [self.__class__(*args[:-1]), args[-1]]
            elif self.order == self.RIGHT_TO_LEFT:
                args = [args[0], self.__class__(*args[1:])]

        super(Noncommutative, self).__init__(*args)

    def __hash__(self):
        return hash(tuple(self.children))


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

    def __mul__(self, other):
        return Number(self.number * other.number)

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

