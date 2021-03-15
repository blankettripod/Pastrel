import Token
import Error



L_NUMBERS = '0123456789.'
L_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
L_OPERATORS = '+-*/%^'

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.errors = []
        self.line = 0
        self.i = 0

    def getPointFromLine(self, x):
        lines = self.code.splitlines()
        point = 0
        for i in range(len(lines)):
            if i == self.line:
                break
            point += len(lines[i])
        return x-point-self.line

        
    def lex(self):
        self.line = 0
        while self.i < len(self.code): #this is a while loop because generating numbers changes the index

            if self.code[self.i] == '\n': # increment line number
                self.line += 1
                self.tokens.append(Token.Token("newline", None, self.getPointFromLine(self.i), self.getPointFromLine(self.i)))

            elif self.code[self.i] in [' ', '\t']: # whitespace
                pass

            elif self.code[self.i] in L_NUMBERS: # number
                self.tokens.append(self.number())

            elif self.code[self.i] in L_LETTERS: # identifier
                self.tokens.append(self.identifier())
                continue

            elif self.code[self.i] in L_OPERATORS: # operator
                self.tokens.append(Token.Token(self.code[self.i], None, self.getPointFromLine(self.i), self.getPointFromLine(self.i)))

            elif self.code[self.i] == '(':
                self.tokens.append(Token.Token('(', None, self.getPointFromLine(self.i), self.getPointFromLine(self.i)))

            elif self.code[self.i] == ')':
                self.tokens.append(Token.Token(')', None, self.getPointFromLine(self.i), self.getPointFromLine(self.i)))

            else: # unexpected character
                self.errors.append(Error.Error(f"unexpected character {self.code[self.i]}", self.line, self.getPointFromLine(self.i), self.getPointFromLine(0), self.code))
            
            self.i += 1

    def number(self):
        decimals = 0
        string = ''
        start = self.i

        if self.code[self.i] == '.': # for numbers like .1
            decimals = 1
            self.i += 1

        while self.i < len(self.code) and self.code[self.i] in L_NUMBERS: # while text is still a number
            string += self.code[self.i]
            if self.code[self.i] == '.': # check for decimal
                decimals += 1
                if decimals > 1: # two decimal points in number
                    self.errors.append(Error.Error(f"invalid string literal {decimals} ", self.line, self.getPointFromLine(start), self.i-start+1, self.code))
                    return 1

            self.i += 1

        if self.i < len(self.code) and self.code[self.i] == 'f': # float
            return Token.Token('float', float(string), start, self.i)
        elif decimals == 1: # double
            self.i -= 1
            return Token.Token('double', float(string), start, self.i)
        else: # int
            self.i -= 1
            return Token.Token('int', int(string), start, self.i)

    def identifier(self):
        string = ''
        start = self.i
        while self.i < len(self.code) and self.code[self.i] in L_LETTERS:
            string += self.code[self.i]
            self.i += 1
        return Token.Token("identifier", string, start, self.i)
