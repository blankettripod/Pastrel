import Token
import Lexer
import Parser
import Semantics
import codeGeneration
import assembler


while True:
    inp = input('>>>')

    if inp == 'q' or inp == 'quit':
        break

    l = Lexer.Lexer(inp.replace('~', '\n'))
    l.lex()
    if len(l.errors) > 0:
        for error in l.errors:
            print(error)
        continue

    print(l.tokens)
    
    p = Parser.Parser(l.tokens, inp)
    p.Parse()
    if len(p.errors) > 0:
        for error in p.errors:
            print(error)
        continue
    for node in p.tree:
        print(node)


