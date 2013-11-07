import string
from array import array
from decimal import Decimal as D
from collections import deque, OrderedDict
from operators import *


class ParseError(Exception):
    pass


class EquationParser(object):
    def parse(self, equation):
        """
        Preprocess the equation before feeding it to the parser.

        1. Removes spaces.
        2. Changes minus operators into + -n.
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
            ('/', Fraction),
            ('+', Plus),
        ])
        ORDER_OF_OPERATIONS = ['^', '*/', '+']
        OPEN_BRACKETS = "({["
        CLOSE_BRACKETS = "]})"

        symbols = []
        operators = []

        is_letter = lambda x: x.lower() in string.lowercase
        is_number = lambda x: x in '0123456789.'
        parse_number = lambda x: D(x) if '.' in x else int(x)

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
            char = equation.popleft()

            if char in OPERATOR_TO_CLASS_MAP.keys():
                operators.append(char)

            elif char in OPEN_BRACKETS:
                symbols.append(Brackets(self._parse(equation)))

            elif char in CLOSE_BRACKETS:
                break

            # must be a negative sign, since subtraction is changed into + -n.
            elif char == '-':
                symbols.append(-1)
                operators.append('*')

            elif is_number(char):
                n = char + match_sequence(equation, is_number)
                symbols.append(parse_number(n))

            elif is_letter(char):
                symb = char + match_sequence(equation, is_letter)
                symbols.append(symb)

        # parse symbol and operator lists into expression tree, following order of operations
        for current_op in ORDER_OF_OPERATIONS:
            index = 0
            while index < len(operators):
                op = operators[index]
                symbs = []
                if operators[index] in current_op:
                    # this is the beginning of an operator chain (i.e. 4 * x * y * x)
                    while index < len(operators) and operators[index] == op:
                        symbs.append(symbols.pop(index))
                        operators.pop(index)
                    symbs.append(symbols.pop(index))
                    symbols.insert(index, OPERATOR_TO_CLASS_MAP[op](*symbs))
                else:
                    index += 1

        return symbols[0]
