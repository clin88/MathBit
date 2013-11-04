from abc import ABCMeta

class BaseOperator(object):
   sign = '?'
   def __init__(self, *args):
      self.args = args

   def __repr__(self):
      sign = "%s %s %s"
      return reduce(lambda x, y: sign % (str(x), self.sign, str(y)), self.args)

   def __treerepr__(self):
      sign = "%s %s %s"
      return "(" + reduce(lambda x, y: sign % (str(x), self.sign, str(y)), self.args) + ")"

class Expr(BaseOperator):
   def __repr__(self):
      s = "(%s)"
      return s % super(Expr, self).__repr__()


class Plus(BaseOperator):
   sign = '+'

class Mult(BaseOperator):
   sign = '*'

class Pow(BaseOperator):
   sign = '^'

class Minus(BaseOperator):
   sign = '-'

class Division(BaseOperator):
   sign = '/'
