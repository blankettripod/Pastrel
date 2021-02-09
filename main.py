import Lexer
import Parser

lexed = Lexer.lex("2+2")
parser = Parser.Parser(lexed)
parsed = parser.parse()
print(parsed)