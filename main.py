import Token
import Lexer
import Parser
import Semantics
import codeGeneration

# import sys

while True:
    inp = input('>>> ')
    if inp == 'quit' or inp == 'q':
        break

    l = Lexer.Lexer(inp)
    l.lex()
    print(f'Tokens: {l.tokens}')
    if len(l.errors) > 0:
        for error in l.errors:
            print(error)
        continue
    
    p = Parser.Parser(l.tokens)
    p.Parse()
    print(f'Nodes: {p.tree}')
    if len(p.errors) > 0:
        for error in p.errors:
            print(error)
        continue
    
    s = Semantics.checker(p.tree)
    s.check()
    if len(s.errors) > 0:
        for error in s.errors:
            print(error)
        continue
    
    
    c = codeGeneration.Generator(p.tree)
    c.generate()

    print(f'Code: {c.code}')
    print(f'Memory: {c.memory}')
    
    