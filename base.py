"""
Definitions for low level, base operator classes.
"""
from functools import total_ordering


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

            Sets parent property.
        """
        from numbers import Number as N
        from operators import Number, Symbol

        for arg in args:
            if isinstance(arg, N):
                arg = Number(arg)
            elif isinstance(arg, str):
                arg = Symbol(arg)

            arg.parent = self
            self._children.append(arg)

    def replace_child(self, index, child):
        self._children[index] = child
        child.parent = self

    def pop_child(self, index=None):
        if index != None:
            return self._children.pop(index)
        else:
            return self._children.pop()

    def insert_child(self, index, *children):
        for delta, child in enumerate(children):
            self._children.insert(index + delta, child)
            child.parent = self

    def replace_self(self, arg):
        for index, item in enumerate(self.parent.children):
            if id(item) == id(self):
                self_index = index
                break

        self.parent.replace_child(self_index, arg)


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


class Commutative(Operator):
    pass