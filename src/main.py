import sys

import Token
import Utility
import Lexer
import Parser

longRule = Parser.Rule("long", ["long"])
intRule = Parser.Rule("int", ["int"])
doubleRule = Parser.Rule("double", ["double"])
floatRule = Parser.Rule("float", ["float"])


numberRule = Parser.Rule("number", [(intRule, longRule, floatRule, doubleRule)])


multiplyRule = Parser.Rule("multiply", [{"*"}])
divideRule = Parser.Rule("divide", [{"/"}])

addRule = Parser.Rule("addition", [{"+"}])
subRule = Parser.Rule("subtraction", [{"-"}])

factorMD = Parser.Rule("factorMD", ["number", (multiplyRule, divideRule), "number"])
factorAS = Parser.Rule("factorAS", ["number", (addRule, subRule)])

factor = Parser.Rule("factor", ["factorAS", "factorMD"])
factor2 = Parser.Rule("factor", ["factorAS", "factor"])
factor3 = Parser.Rule("factor", ["factorAS", "number"])
factor4 = Parser.Rule("factor", ["factorMD", Parser.T_TYPE_ARITHMETIC, "number"])

rules = [
    numberRule,
    factorMD,
    factorAS,
    factor,
    factor2,
    factor3,
    factor4,
]


lexer = Lexer.Lexer("2*2*3")
lexer.Lex()

for token in lexer.tokens:
    print(token)

for error in lexer.errors:
    print(error.Assert())

parser = Parser.Parser(lexer.tokens, rules)
output = parser.parse()

for value in output:
    print(value)
    print("\n")
