from output import PrintToConsole
import parse
from simplifier import Simplifier

s = Simplifier(PrintToConsole())
p = parse.EquationParser()
s.simplify(p.parse("x * x / y * x"))
