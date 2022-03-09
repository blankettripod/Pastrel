#pragma once

#include <cstddef>

#include <vector>

#include <Stages/Common/Error.h>
#include <Stages/Common/Token.h>
#include <Stages/Common/Node.h>

#define currentToken state.stream.at(state.index)

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
                std::vector<Common::Token> stream;

                // use a union to pack two types into one vector
                std::vector<Common::CommonNode> stack;

                // the output of the parser
                std::vector<Common::Node> nodes;

                // any errors when parsing
                std::vector<Common::Error::Error> errors;
            };  

            bool StateIsValid(const ParserState& state) noexcept {
                return (state.index < state.stream.size() && state.stream.size() > 0);
            }

            void ShiftStack(ParserState& state) noexcept {
                // the next token is pointed at by the state index
                state.stack.push_back(currentToken);
                // increment the state index to look at the new lookahead
            }

            Common::Token& GetLookahead(const ParserState& state) noexcept {
                // the lookahead is pointed to by the state index
                return currentToken;
            }


            void ParseCode(ParserState& state) noexcept {
                if (!StateIsValid(state)) return;

                // clear the state to allow for multiple runs
                state.index = 0;
                state.nodes.clear();
                state.errors.clear();
                
                /*
                    ALGORITHM

                    this is a shift reduce lr(1) parser
                    it has three sections for storing tokens
                    
                    the stack, lookahead and the stream

                    the stack contains the working tokens, 
                    this is tokens that have been read by the parser and are check against patterns 

                    the lookahead is where precedence calculations are taking place

                    the stream is the tokens that have not yet been added to the stack or lookahead


                    how it works is a token is taken from the stream and added to the stack,
                    then another is taken from the stream and added to the lookahead
                    it then has all the patterns checked against it 
                    (using precedence i.e. multiply before add)
                    if no patterns are found, the index to check from is incremented by one.

                    e.g. 

                    2, +, 2, *, 2.
                    ^
                    first it will check the entire stack for a pattern
                    since it is not valid it will return a fail
                    it will then increment the pointer and check the stack from index 1 to the end

                    2, +, 2, *, 2.
                    ^~~~

                    this will repeat untill a pattern is found

                    2, +, 2, *, 2.
                    ^~~~~~~

                    one a pattern is found, the parser will "reduce" the stack by
                    collapsing the matched tokens into a node

                    node(bin_op), *, 2
                    

                    the stack pointer is then put back to the start

                    node(bin_op), *, 2
                    ^~~~~~~~~~~~

                    if nothing is found by the time the pointer has reached the end then the base index will be moved right
                    e.g.
                    2, +, 2, *, 2
                       ^
                    2, +, 2, *, 2
                       ^~~~
                    2, +, 2, *, 2
                       ^~~~~~~


                    only one the base pointer reaches the last token without finding anything 
                    will another token be taken from the stream and added to the stack (and lookahead)

                    the lookahead is used to determine whether a pattern should be accepted or not

                    e.g. in the example above. the first pattern would be the 2, +, 2 
                    but since the lookahead is a multiply token (which has a higher precedence)
                    this means that the pattern would not usually be accepted because otherwise it would mess with 
                    the ordering of bodmas
                */


                size_t base = state.index;

            }


        } 
    }
}
