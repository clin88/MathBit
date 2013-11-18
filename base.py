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

