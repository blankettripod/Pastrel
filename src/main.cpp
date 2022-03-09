#include <iostream>
#include <sstream>

#include <cmath>

#include <Pastrel.h>

const std::string TestCode("2d + 3 * 4");



int main(int argc, char** argv) {

    const char* filename = Pastrel::Utility::Arguments::cmdOptionExists(argv, argv+argc, std::string("-f"))?
                           Pastrel::Utility::Arguments::getCmdOption(argv, argv+argc, std::string("-f")):
                           nullptr;

    if (filename == nullptr) {
        std::cout << "file not specified\n\n";
    }


    std::ostringstream code;
    
    code << ((filename != nullptr)? Pastrel::Utility::File::ReadFile(filename) : TestCode);

    std::cout << "Code: \n" << code.str() << "\n\n";

    Pastrel::Stages::Lexer::LexerState lexerState{};


    lexerState.code = code.str().c_str();
    lexerState.filename = filename != nullptr? filename:"<stdio>";

    Pastrel::Stages::Lexer::LexCode(lexerState);
    
    Pastrel::Stages::Parser::ParserState parserState{};

    parserState.code = code.str().c_str();
    parserState.filename = filename != nullptr? filename:"<stdio>";

    Pastrel::Stages::Parser::ParseCode(parserState);




    // print all the tokens and their types
    std::cout << "Tokens:\n";
    for (const auto& token : lexerState.tokens) {

        switch (token.type) {
            case T_TYPE_IDENTIFIER:
                std::cout << "\tIndentifier: " << token.values.sType << '\n';
                break;
            case T_TYPE_INTEGER:
                std::cout << "\tInteger: " << token.values.iType << '\n';
                break;
            case T_TYPE_UNSIGNED_INTEGER:
                std::cout << "\tUnsigned Integer: " << token.values.uType << '\n';
                break;
            case T_TYPE_LONG:
                std::cout << "\tLong: " << token.values.iType << '\n';
                break;
            case T_TYPE_UNSIGNED_LONG:
                std::cout << "\tUnsigned Long: " << token.values.uType << '\n';
                break;
            case T_TYPE_FLOAT:
                std::cout << "\tFloat: " << static_cast<float>(token.values.fType) << '\n';
                break;
            case T_TYPE_DOUBLE:
                std::cout << "\tDouble: " << token.values.fType << '\n';
                break;
            case T_TYPE_BOOLEAN:
                std::cout << "\tBool: " << token.values.bType << '\n';
                break;
            case T_TYPE_OPERATOR:
                std::cout << "\tOperator: " << token.values.sType << '\n';
                break;
            case T_TYPE_STRING:
                std::cout << "\tString: " << token.values.sType << '\n';
                break;
            case T_TYPE_CHAR:
                std::cout << "\tCharacter: " << token.values.cType << "\n";
                break;
            default:
                break;
        }
    }

    for (const auto& error : lexerState.errors) {
        std::cout << Pastrel::Stages::Common::Error::CreateError(error) << '\n';
    }

    std::cout << "\nNumber of tokens: "  << lexerState.tokens.size() << std::endl;

    if (lexerState.errors.size() > 0) return -1;

    

    return 0;
}