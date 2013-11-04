from parse import *
from pprint import pprint

def test_parse():
   test_cases = [
      '3 * (5 + 4 * x) + 3 + (6 * x)',
      '3 * x + 4 + 5 + 4 * y',
      '43 * x + 4 + 5 + 4 * y',
      r'4*x^2 + z',
      'a*b*c* d*e',
      '1.034 * x',
   ]
   parser = EquationParser()

   for case in test_cases:
      print case
      pprint(parser.parse(case))

test_parse()
