#include <iostream>
#include <sstream>

#include <Pastrel.h>

const std::string TestCode("2+a");



int main(int argc, char** argv) {

    const char* filename = Pastrel::Utility::Arguments::cmdOptionExists(argv, argv+argc, std::string("-f"))?
                           Pastrel::Utility::Arguments::getCmdOption(argv, argv+argc, std::string("-f")):
                           nullptr;

    if (filename == nullptr) {
        std::cout << "file not specified\n";
    }


    std::ostringstream code;
    
    code << ((filename != nullptr)? Pastrel::Utility::File::ReadFile(filename) : TestCode);

    std::cout << code.str() << std::endl;

    Pastrel::Stages::Lexer::LexerState state{};

    state.code = code.str().c_str();
    state.filename = filename != nullptr? filename:"<stdio>";

    int result = Pastrel::Stages::Lexer::LexCode(state);


    for (const auto& token : state.tokens) {

        switch (token.type) {
            case T_TYPE_IDENTIFIER:
                std::cout << "Indentifier: " << token.values.sType << '\n';
                break;
            case T_TYPE_INTEGER:
                std::cout << "Integer: " << token.values.iType << '\n';
                break;
            case T_TYPE_UNSIGNED_INTEGER:
                std::cout << "Unsigned Integer: " << token.values.uType << '\n';
                break;
            case T_TYPE_FLOAT:
                std::cout << "Float: " << static_cast<float>(token.values.fType) << '\n';
                break;
            case T_TYPE_DOUBLE:
                std::cout << "Double: " << token.values.fType << '\n';
                break;
            case T_TYPE_BOOLEAN:
                std::cout << "Bool: " << token.values.bType << '\n';
            default:
                break;
        }
    }

    for (const auto& error : state.errors) {
        std::cout << Pastrel::Stages::Common::Error::CreateError(error) << '\n';
    }


    return result;
}