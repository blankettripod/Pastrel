import Utility
from Error import *
from Token import *

L_NUMBERS = '.0123456789'
L_WHITESPACE = ' \t\n'
L_ARITHMETIC_OPERATORS = '+-*/'
L_CONDITIONAL_OPERATORS = '=<>'
L_EXTENDED_CONDITIONAL_OPERATORS = ['==', '>=', '<=', '!=']
L_MISC_OPERATORS = "()[]{}<>?:;"
L_STRING_STARTERS = "'\""
L_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
L_KEYWORDS = (
    "return",
    "while",
    "for",
    "if",
    "else",
    "int",
    "double",
    "float",
    "long",
    "string"
)


class Lexer:
    tokens: list[Token]
    i: int
    code: str
    errors = list[Error]
    line: int = 0

    def __init__(self, code: str = "") -> None:
        self.code = code
        self.line = 0
        self.errors = []
        self.tokens = []
        self.i = 0

    def Lex(self) -> list[Token]:
        while self.i < len(self.code):
            if self.code[self.i] == '\n':
                self.line += 1
            elif self.code[self.i] in L_WHITESPACE:
                pass
            elif self.code[self.i] in L_NUMBERS:
                self.tokens.append(self.GenerateNumber())

            elif self.code[self.i] in L_ARITHMETIC_OPERATORS:
                self.tokens.append(Token(T_TYPE_ARITHMETIC, self.code[self.i]))

            elif self.code[self.i] in L_CONDITIONAL_OPERATORS:
                self.tokens.append(Token(T_TYPE_CONDITIONAL, self.code[self.i]))

            elif self.code[self.i] in L_STRING_STARTERS:
                self.tokens.append(self.GenerateString())

            elif self.code[self.i] in L_CHARACTERS:
                self.tokens.append(self.GenerateIdentifier())

            else:
                self.errors.append(Error("L0001", f"Illegal Character {self.code[self.i]}"))
            self.i += 1

        return self.tokens



    def GenerateIdentifier(self) -> Token:
        output = ""

        while self.i < len(self.code) and self.code[self.i] in L_CHARACTERS:
            output += self.code[self.i]
            self.i += 1

        self.i -= 1
        if output in L_KEYWORDS:
            return Token(T_TYPE_KEYWORD, output)
        else:
            return Token(T_TYPE_IDENTIFIER, output)

    def GenerateString(self) -> Token:
        starter = self.code[self.i]
        output = ""
        self.i += 1

        while self.i < len(self.code) and self.code[self.i] != starter:
            output += self.code[self.i]
            self.i += 1

        if self.i >= len(self.code):
            self.errors.append(Error("L0003", "string Isn't Terminated"))

        return Token(T_TYPE_STRING, output)

    def GenerateNumber(self) -> Token:
        output = ''
        decimals = 0
        start = self.i

        while self.i < len(self.code) and self.code[self.i] in L_NUMBERS:
            if self.code[self.i] == '.':
                decimals += 1
                if decimals > 1:
                    self.errors.append(Error("L0002", "Invalid Number Literal"))
                    return Token(T_TYPE_ERROR)
                output += '.'
            else:
                output += self.code[self.i]
            self.i += 1

        if self.i < len(self.code):
            if self.code[self.i] == 'f':
                return Token(T_TYPE_FLOAT, float(output))

            elif self.code[self.i] == 'l':
                if decimals != 0:
                    self.errors.append(Error("L0002", "Invalid Long literal"))
                    return Token(T_TYPE_ERROR)

                return Token(T_TYPE_LONG, int(output))

        if decimals == 1 or (self.i < len(self.code) and self.code[self.i] == 'd'):
            return Token(T_TYPE_DOUBLE, float(output))

        else:
            self.i -= 1
            return Token(T_TYPE_INT, int(output))
