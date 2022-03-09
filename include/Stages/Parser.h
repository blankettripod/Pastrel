#pragma once

#include <cstddef>

#include <vector>
#include <map>

#include <Stages/Common/Error.h>
#include <Stages/Common/Token.h>
#include <Stages/Common/Node.h>
#include <Stages/Common/Rule.h>

#define currentToken state.stream.at(state.index)

// start at 12 because thats where tokens left off. this allows easier type checking as only one value is needed
#define P_RULE_NUMBER 12ul
#define P_RULE_FACTOR 13ul
#define P_RULE_BINOP  14ul

namespace Pastrel
{
    namespace Stages
    {  
        namespace Parser
        {

            std::map<const char*, size_t> LiteralPrecedences = {
                {"+", 3},                
                {"-", 3},                
                {"*", 4},                
                {"/", 4},                
            };

            std::map<size_t, size_t> TokenPrecedences = {
            };

            // all the rules used by the parser
            constexpr Rule rules[] = {
                // numbers are immediately converted into a common type. this is because typechecking is done in the next stage, so we don't need to bother
                {P_RULE_NUMBER, 64, {
                    {R_TYPE_TYPE, R_MODIFIER_CHOICE, {
                        {T_TYPE_INTEGER},
                        {T_TYPE_UNSIGNED_INTEGER},
                        {T_TYPE_LONG},
                        {T_TYPE_UNSIGNED_LONG},
                        {T_TYPE_FLOAT},
                        {T_TYPE_DOUBLE}
                    }},
                }},

                // a multiply divide operation can be done on anything
                {P_RULE_BINOP, 4, {
                    {R_TYPE_RULE, R_MODIFIER_STOCK, {P_RULE_FACTOR}},
                    {R_TYPE_LITERAL, R_MODIFIER_CHOICE, {
                        {0ul, "*"},
                        {0ul, "/"}
                    }},
                    {R_TYPE_RULE, R_MODIFIER_STOCK, {P_RULE_FACTOR}},
                }},

                {P_RULE_BINOP, 4, {
                    {R_TYPE_RULE, R_MODIFIER_STOCK, {P_RULE_NUMBER}},
                    {R_TYPE_LITERAL, R_MODIFIER_CHOICE, {
                        {0ul, "*"},
                        {0ul, "/"}
                    }},
                    {R_TYPE_RULE, R_MODIFIER_STOCK, {P_RULE_FACTOR}},
                }},

                {P_RULE_BINOP, 4, {
                    {R_TYPE_RULE, R_MODIFIER_STOCK, {P_RULE_FACTOR}},
                    {R_TYPE_LITERAL, R_MODIFIER_CHOICE, {
                        {0ul, "*"},
                        {0ul, "/"}
                    }},
                    {R_TYPE_RULE, R_MODIFIER_STOCK, {P_RULE_NUMBER}},
                }},

                // factors can be made from number but are not allowed to collapse
                {P_RULE_FACTOR, 3, {
                    {R_TYPE_RULE, R_MODIFIER_STOCK, {P_RULE_NUMBER}},
                }},

                {P_RULE_FACTOR, 3, {
                    {R_TYPE_RULE, R_MODIFIER_STOCK, {P_RULE_BINOP}},
                }},

                {P_RULE_BINOP, 3, {
                    {R_TYPE_RULE, R_MODIFIER_STOCK, {P_RULE_FACTOR}},
                    {R_TYPE_LITERAL, R_MODIFIER_CHOICE, {
                        {0ul, "+"},
                        {0ul, "-"}
                    }},
                    {R_TYPE_RULE, R_MODIFIER_STOCK, {P_RULE_FACTOR}},
                }},
            };


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

                Common::CommonNode node;

                node.type = 1;
                node.values.token = &currentToken;

                state.stack.push_back(node);
                // increment the state index to look at the new lookahead
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


                // the starting index for matching patterns
                size_t base = state.index;

                while (StateIsValid(state)) {
                    // add the next token to the stack
                    ShiftStack(state);

                    // check all paterns against the stack
                    for (int base = 0; base < state.stack.size(); ++base){
                        for (int length = state.stack.size() - base; length > 0; --length){

                            // check items from base to base+length against every rule

                            for (const auto& rule : rules) {

                            }




                        }
                    }
                }

            }


        } 
    }
}
