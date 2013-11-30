class Cursor(object):
    """
        Rudimentary api for "zipper" data structure. Enables efficient
        and easy traversal and manipulation for immutable trees.

        All nodes should inherit from tuple. Leafs can be arbitrary types.
    """
    def __init__(self, node, left_siblings, up, right_siblings):
        self._node = node
        self._left_siblings = left_siblings
        self._up = up
        self._right_siblings = right_siblings

    def __repr__(self):
        return repr(self.node)

    @property
    def node(self):
        return self._node

    def top(self):
        cursor = self
        while cursor.can_up():
            cursor = cursor.up()

        return cursor

    def can_up(self):
        return bool(self._up)

    def up(self):
        if not self.can_up():
            raise IndexError("No room to move up on tree.")

        up = self._up
        children = self._left_siblings + (self.node,) + self._right_siblings
        node = up.node.__class__(children)
        return Cursor(node=node,
                      left_siblings=up._left_siblings,
                      up=up._up,
                      right_siblings=up._right_siblings)

    def can_left(self):
        return bool(self._left_siblings)

    def left(self):
        if not self.can_left():
            raise IndexError("No room to move left on tree.")

        return Cursor(node=self._left_siblings[-1],
                      left_siblings=self._left_siblings[:-1],
                      up=self._up,
                      right_siblings=(self._node,) + self._right_siblings)

    def can_right(self):
        return bool(self._right_siblings)

    def right(self):
        if not self.can_right():
            raise IndexError("No room to move right on tree.")

        return Cursor(node=self._right_siblings[0],
                      left_siblings=self._left_siblings + (self._node,),
                      up=self._up,
                      right_siblings=self._right_siblings[1:])

    def can_down(self):
        return bool(isinstance(self._node, tuple) and self._node)

    def down(self):
        if not self.can_down():
            raise IndexError("No room to move down on tree.")

        return Cursor(node=self._node[0],
                      left_siblings=(),
                      up=self,
                      right_siblings=self._node[1:])

    def insert_left(self, node):
        return Cursor(node=self._node,
                      left_siblings=self._left_siblings + (node,),
                      up=self._up,
                      right_siblings=self._right_siblings)

    def insert_right(self, node):
        return Cursor(node=self._node,
                      left_siblings=self._left_siblings,
                      up=self._up,
                      right_siblings=(node,) + self._right_siblings)

    def insert_down(self, node):
        node = self.node.__class__(self.node + (node,))
        return self.replace_self(node)

    def replace_self(self, node):
        return Cursor(node=node,
                      left_siblings=self._left_siblings,
                      up=self._up,
                      right_siblings=self._right_siblings)

def make_cursor(root):
    """
        Creates a cursor from the root node of a tree.
    """
    return Cursor(node=root,
                  left_siblings=(),
                  up=None,
                  right_siblings=())
