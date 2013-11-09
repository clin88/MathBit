"""
Definitions for low level, base operator classes.
"""


class Node(object):
    def __init__(self, *args, **kwargs):
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, arg):
        self._parent = arg


class BaseOperator(Node):
    sign = '?'

    def __init__(self, *args):
        self._children = []
        self.add_children(*list(args))
        super(BaseOperator, self).__init__(*args)

    def __repr__(self):
        # when parent has operator precedence, show parenthesis to indicate priority:
        #   e.g. Mult(Plus(4, 5), 3): 4 + 5 * 3 -> (4 + 5) * 3

        sign = "%s %s %s"
        if len(self.children) > 1:
            rep = reduce(lambda x, y: sign % (str(x), self.sign, str(y)), self.children)
        else:
            rep = str(self.children[0])

        if self.parent.oop <= self.oop:
            return '(%s)' % rep
        else:
            return rep

    def __eq__(self, other):
        if not isinstance(other, BaseOperator):
            return False

        if len(self.children) != len(other.children):
            return False

        for left, right in zip(self.children, other.children):
            if left != right:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

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

    def replace_child(self, index, arg):
        self._children[index] = arg
        arg.parent = self

    def pop_child(self, index):
        self._children.pop(index)

    def insert_child(self, index, child):
        self._children.insert(index, child)
        child.parent = self


class Noncommutative(BaseOperator):
    """
    Describes noncommutative operators. These should be parsed (using division as an example):

    left = (1, 2, 3) -> ((1, 2), 3)
    e.g. division: 1 / 2 / 3 == (1 / 2) / 3

    right = (1, 2, 3) -> (1, (2, 3))
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