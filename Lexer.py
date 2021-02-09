import string
import Tokens

NUMBERS = "0123456789."
WHITESPACE = " \t\0"
LETTERS = string.ascii_letters

LETTERS_NUMBERS = LETTERS + NUMBERS


def lex(codes):
    i = 0
    codes += '\0'
    codez = codes.split('\n')
    token = []
    for code in codez:
        i=0
        tokens = []
        while i < len(code):
            if code[i] in NUMBERS:
                num, i = generate_number(code, i)
                if num.type == "Error":
                    print(num.value)
                    return []
                else:
                    tokens.append(num)
            elif code[i] in LETTERS:
                ident, i = generate_identifier(code, i)
                tokens.append(ident)
            elif code[i] in WHITESPACE:
                i += 1
                pass
            elif code[i] == '+':
                tokens.append(Tokens.Token("+"))
                i += 1
            elif code[i] == '-':
                tokens.append(Tokens.Token("-"))
                i += 1
            elif code[i] == '*':
                tokens.append(Tokens.Token("*"))
                i += 1
            elif code[i] == '/':
                tokens.append(Tokens.Token("/"))
                i += 1
            elif code[i] == '%':
                tokens.append(Tokens.Token("%"))
                i += 1
            elif code[i] == '^':
                tokens.append(Tokens.Token("^"))
                i += 1
            elif code[i] == '|':
                tokens.append(Tokens.Token("|"))
                i += 1
            elif code[i] == '&':
                tokens.append(Tokens.Token("&"))
                i += 1
            elif code[i] == '~':
                tokens.append(Tokens.Token("~"))
                i += 1
            elif code[i] == '<':
                tokens.append(Tokens.Token("<"))
                i += 1
            elif code[i] == '>':
                tokens.append(Tokens.Token(">"))
                i += 1
            elif code[i] == '(':
                tokens.append(Tokens.Token("("))
                i += 1
            elif code[i] == ')':
                tokens.append(Tokens.Token(")"))
                i += 1
            elif code[i] == ':':
                tokens.append(Tokens.Token(":"))
                i += 1
            elif code[i] == ';':
                tokens.append(Tokens.Token("end"))
                i += 1
            elif code[i] == '=':
                tokens.append(Tokens.Token("="))
                i += 1
            elif code[i] == "'":
                out, i = generate_string(code, i)
                tokens.append(out)
                i += 1
            elif code[i] == ',':
                tokens.append(Tokens.Token(","))
                i += 1
            elif code[i] == '{':
                tokens.append(Tokens.Token("{"))
                i += 1
            elif code[i] == '}':
                tokens.append(Tokens.Token("}"))
                i += 1
            else:
                print(f"Error: Invalid Character {code[i]}")
                return []
        token.append(tokens)
    return token


def generate_identifier(code, i):
    identifier = code[i]
    i += 1
    while code[i] in LETTERS_NUMBERS:
        identifier += code[i]
        i += 1

    return Tokens.Token("Identifier", identifier), i


def generate_number(code, i):
    number = code[i]
    i += 1
    dots = 0
    if code[i-1] == '.':
        dots += 1
    while code[i] in NUMBERS:
        if code[i] == ".":
            dots += 1
        if dots > 1:
            return [Tokens.Token("Error", "Invalid Number"), i]
        number += code[i]
        i += 1

    if dots > 0:
        if code[i] == "f":
            i += 1
            if number[0] == '.':
                number = '0' + number
            return Tokens.Token("float", float(number)), i
        else:
            return Tokens.Token("double", float(number)), i
    else:
        if code[i] == "f":
            i += 1
            return Tokens.Token("float", float(number)), i
        else:
            return Tokens.Token("int", int(number)), i


def generate_string(code, i):
    identifier = ''
    i += 1
    while code[i] != "'":
        identifier += code[i]
        i += 1

    return Tokens.Token("string", identifier), i

