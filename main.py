import Lexer
import Parser

output = Lexer.lex("int main() { return 2 }")
parser = Parser.Parser(output)
parsed = parser.parse()
print(parsed)
