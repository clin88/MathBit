import string
from array import array
from collections import deque, OrderedDict
from operators import *


class EquationParser(object):
    def parse(self, equation):
        """
        Preprocess the equation before feeding it to the parser.

        1. Removes spaces.
        2. Changes implicit multiplication into explicit (xy -> x * y; (-(a + b) -> -1 * (a + b))
        3. Passes through a deque object.
        """
        return Expr(self._parse(deque(equation)))

    def _parse(self, equation):
        """
        Parses an equation in canonical format into an expression tree.

        Don't call directly--let parse() preprocess the equation first.
        """
        OPERATOR_TO_CLASS_MAP = OrderedDict([
            ('^', Exp),
            ('*', Mult),
            ('/', Fraction),
            ('+', Plus),
            ('=', Eq)
        ])
        ORDER_OF_OPERATIONS = ['^', '*/', '+', '=']
        OPEN_BRACKETS = "({["
        CLOSE_BRACKETS = "]})"

        symbols = []
        operators = []

        is_letter = lambda x: x.lower() in string.lowercase
        is_number = lambda x: x in '-0123456789.'

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
                symbols.append(self._parse(equation))

            elif char in CLOSE_BRACKETS:
                break

            elif char == '=':
                symbols.append(self._parse(equation))
                operators.append(char)

            elif is_number(char):
                n = char + match_sequence(equation, is_number)
                symbols.append(Number(n))

            elif is_letter(char):
                symb = char + match_sequence(equation, is_letter)
                symbols.append(Symbol(symb))

        # parse symbol and operator lists into expression tree, following order of operations
        for current_op in ORDER_OF_OPERATIONS:
            index = 0
            while index < len(operators):
                op = operators[index]
                if op not in current_op:
                    index += 1
                    continue

                # this is the beginning of an operator chain (i.e. 4 * x * y * x)
                symbs = []
                while index < len(operators) and operators[index] == op:
                    symbs.append(symbols.pop(index))
                    operators.pop(index)
                symbs.append(symbols.pop(index))
                symbols.insert(index, OPERATOR_TO_CLASS_MAP[op](*symbs))

        return symbols[0]