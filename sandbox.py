import math
import numpy as np
import sys
from sympy import *
from sympy import symbols, Eq, solve

p2_alt1_top  = 4
p2_alt1_bot  = 6
p2_alt2_top  = 5
p2_alt2_bot  = 9
print(type(p2_alt2_bot))
print(p2_alt1_top)
print(p2_alt1_bot)
print(p2_alt2_top)
print(p2_alt2_bot)
q = symbols('q')
exprA = q*p2_alt1_top + (1-q)*p2_alt1_bot
exprB = q*p2_alt2_top + (1-q)*p2_alt2_bot
solution = solve(Eq(exprA, exprB),q)
print(bool(solution))
print(solution[0])
print(solution[0] + 1)
print(type(solution[0]))
print(float(solution[0])+ 1)
print(type(float(solution[0])+ 1))
