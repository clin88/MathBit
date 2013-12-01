import string
from array import array
from collections import deque, OrderedDict
from ops import *
from decimal import Decimal


def num(s):
    try:
        return int(s)
    except ValueError:
        return Decimal(s)

def parse(equation):
    """
    Preprocess the equation before feeding it to the parser.

    1. Removes spaces.
    2. Changes implicit multiplication into explicit (xy -> x * y; (-(a + b) -> -1 * (a + b))
    3. Passes through a deque object.
    """
    return _parse(deque(equation))

def _parse(equation):
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

    is_letter = lambda x: x.lower() in string.ascii_lowercase
    is_number = lambda x: x in '-0123456789.'

    def match_sequence(equation, match_fn):
        o = array('u')
        while equation:
            if match_fn(equation[0]):
                o.append(equation.popleft())
            else:
                break

        return o.tounicode()

    # parse everything into either a symbol or operator
    while equation:
        char = equation.popleft()

        if char in OPERATOR_TO_CLASS_MAP.keys():
            operators.append(char)

        elif char in OPEN_BRACKETS:
            symbols.append(_parse(equation))

        elif char in CLOSE_BRACKETS:
            break

        elif char == '=':
            symbols.append(_parse(equation))
            operators.append(char)

        elif is_number(char):
            n = char + match_sequence(equation, is_number)
            symbols.append(num(n))

        elif is_letter(char):
            symb = char + match_sequence(equation, is_letter)
            symbols.append(symb)

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
