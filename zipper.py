class Cursor(object):
    """
        Rudimentary api for "zipper" data structure. Enables efficient
        traversal and manipulation for immutable trees.

        All nodes should inherit from tuple. Leafs can be arbitrary types.
    """
    def __init__(self, node, left_siblings, up, right_siblings):
        self.node = node
        self.left_siblings = left_siblings
        self.up = up
        self.right_siblings = right_siblings

    def __repr__(self):
        return repr(self.node)

    def upper(self):
        """Reconstruct parent node.
        """
        children = self.left_siblings + (self.node,) + self.right_siblings
        return self.upnode.__class__(children)

    @property
    def upnode(self):
        return self.up.node

    def top(self):
        cursor = self
        while cursor.can_up():
            cursor = cursor.moveup()

        return cursor

    def can_up(self):
        return bool(self.up)

    def moveup(self):
        if not self.can_up():
            raise IndexError("No room to move up on tree.")

        return self.__class__(node=self.upper(),
                              left_siblings=self.up.left_siblings,
                              up=self.up.up,
                              right_siblings=self.up.right_siblings)

    def canleft(self):
        return bool(self.left_siblings)

    def moveleft(self):
        if not self.canleft():
            raise IndexError("No room to move left on tree.")

        return self.__class__(node=self.left_siblings[-1],
                              left_siblings=self.left_siblings[:-1],
                              up=self.up,
                              right_siblings=(self.node,) + self.right_siblings)

    def canright(self):
        return bool(self.right_siblings)

    def moveright(self):
        if not self.canright():
            raise IndexError("No room to move right on tree.")

        return self.__class__(node=self.right_siblings[0],
                              left_siblings=self.left_siblings + (self.node,),
                              up=self.up,
                              right_siblings=self.right_siblings[1:])

    def can_down(self):
        return bool(isinstance(self.node, tuple) and self.node)

    def movedown(self):
        if not self.can_down():
            raise IndexError("No room to move down on tree.")

        return self.__class__(node=self.node[0],
                              left_siblings=(),
                              up=self,
                              right_siblings=self.node[1:])

    def insert_left(self, node):
        return self.__class__(node=self.node,
                              left_siblings=self.left_siblings + (node,),
                              up=self.up,
                              right_siblings=self.right_siblings)

    def insert_right(self, node):
        return self.__class__(node=self.node,
                              left_siblings=self.left_siblings,
                              up=self.up,
                              right_siblings=(node,) + self.right_siblings)

    def insert_down(self, node):
        # TODO: Fix this
        node = self.node.__class__(self.node + (node,))
        return self.replace(node)

    def replace(self, node):
        return self.__class__(node=node,
                              left_siblings=self.left_siblings,
                              up=self.up,
                              right_siblings=self.right_siblings)

    @classmethod
    def makecursor(cls, root):
        return cls(node=root,
                   left_siblings=(),
                   up=None,
                   right_siblings=())
