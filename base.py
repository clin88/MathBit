"""
Definitions for low level, base operator classes.
"""


class BaseOperator(object):
    sign = '?'

    def __init__(self, *args):
        self.args = list(args)

    def __repr__(self):
        sign = "%s %s %s"
        return "(" + reduce(lambda x, y: sign % (str(x), self.sign, str(y)), self.args) + ")"

    def __treerepr__(self):
        """
        Returns a more verbose representation including class names and expression tree hierarchy.
        """
        sign = "%s %s %s"
        return "(" + reduce(lambda x, y: sign % (str(x), self.sign, str(y)), self.args) + ")"


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
