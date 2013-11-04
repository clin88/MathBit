import re, string
from array import array
from decimal import Decimal as D
from collections import deque, OrderedDict
from operators import *

class ParseError(Exception):
   pass

class OperatorNode(object):
   def __init__(self, symbols):
      self.symbols = symbols


class EquationParser(object):
   def parse(self, equation):
      """
      Preprocess the equation before feeding it to the parser.

      Right now, it just changes implicit multiplication (e.g. 5xy) into explicit using an operator
       (e.g. 5*x*y)
      """
      return self._parse(deque(equation))

   def _parse(self, equation):
      """
      Parses an equation in canonical format into an expression tree.

      Don't call directly--let parse() preprocess the equation first.
      """
      OPERATOR_TO_CLASS_MAP = OrderedDict([
         ('^', Pow),
         ('*', Mult),
         ('/', Division),
         ('+', Plus),
         ('-', Minus)
      ])
      OPERATORS = OPERATOR_TO_CLASS_MAP.keys()
      OPEN_BRACKETS = "({["
      CLOSE_BRACKETS = "]})"
      is_letter = lambda x: x.lower() in string.lowercase
      is_number = lambda x: x in '0123456789.'

      symbols = []
      operators = []

      number_re = re.compile(r'\d*[.]*\d*')
      text_re = re.compile(r'\w+')

      def parse_number(n):
         if '.' in n:
            return D(n)
         else:
            return int(n)

      def match_sequence(equation, match_fn):
         o = array('c')
         while equation:
            if match_fn(equation[0]):
               o.append(equation.popleft())
            else:
               break

         return o.tostring()

      # parse everything into either a symbol or operator
      while equation:
         char = equation[0]

         if char in OPERATORS:
            operators.append(equation.popleft())

         elif char in OPEN_BRACKETS:
            equation.popleft()
            symbols.append(self._parse(equation))

         elif char in CLOSE_BRACKETS:
            equation.popleft()
            break

         elif is_number(char):
            n = match_sequence(equation, is_number)
            symbols.append(parse_number(n))

         elif is_letter(char):
            symbols.append(match_sequence(equation, is_letter))

         else:
            equation.popleft()

      # parse symbol and operator lists into expression tree, following order of operations
      for current_op in OPERATORS:
         index = 0
         while index < len(operators):
            op = operators[index]

            # this is the beginning of an operator chain (i.e. 4 * x * y * x)
            if op == current_op:
               symbs = []
               while index < len(operators) and operators[index] == current_op:
                  symbs.append(symbols.pop(index))
                  operators.pop(index)
               symbs.append(symbols.pop(index))
               symbols.insert(index, OPERATOR_TO_CLASS_MAP[current_op](*symbs))

            index += 1

      return Expr(symbols[0])
