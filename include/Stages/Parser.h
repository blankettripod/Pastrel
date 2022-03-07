#pragma once

#include <cstddef>

#include <vector>

#include <Stages/Common/Error.h>
#include <Stages/Common/Token.h>
#include <Stages/Common/Node.h>

namespace Pastrel
{
    namespace Stages
    {  
        namespace Parser
        {
            struct ParserState {
                // the code that is being worked on
                std::string code;
                // the current position in the code
                size_t index;

                // the file where the code came from, <stdio> if none were supplied
                std::string filename;

                // the output of the lexer
                std::vector<Common::Token> tokens;

                // the output of the parser
                std::vector<Common::Node> nodes;

                // any errors when parsing
                std::vector<Common::Error::Error> errors;
            };  

            bool StateIsValid(const ParserState& state) noexcept {
                return (state.index < state.tokens.size() && state.code.size() > 0);
            }

            void ParseCode(ParserState& state) noexcept {
                if (!StateIsValid(state)) return;

                state.nodes.clear();
                state.errors.clear();
                

                std::vector<size_t>
                


            }


        } 
    }
}
