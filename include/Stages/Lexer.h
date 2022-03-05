#pragma once

#include <cstddef>
#include <cstdint>
#include <cstring>

#include <vector>

#include <string_view>

#include <Stages/Common/Error.h>
#include <Stages/Common/Token.h>

#include <Utility/String.h>

#include <iostream>

#define T_TYPE_IDENTIFIER static_cast<size_t>(1)
#define T_TYPE_INTEGER static_cast<size_t>(2)
#define T_TYPE_UNSIGNED_INTEGER static_cast<size_t>(3)
#define T_TYPE_LONG static_cast<size_t>(4)
#define T_TYPE_UNSIGNED_LONG static_cast<size_t>(5)
#define T_TYPE_FLOAT static_cast<size_t>(6)
#define T_TYPE_DOUBLE static_cast<size_t>(7)
#define T_TYPE_BOOLEAN static_cast<size_t>(8)
#define T_TYPE_OPERATOR static_cast<size_t>(9)

#define currentCharacter state.code.at(state.index)

namespace Pastrel{
    namespace Stages{
        namespace Lexer{

            // all the characters that should be ignored
            const char* WHITESPACE = " \t\n";
            //all the characters that are allowed in identifiers
            const char* ASCII = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_";
            // all numbers including the period
            const char* NUMS = "0123456789.";
            // all operators
            const char* OPERATORS = "()[]{};:'\"\\|&+-*/^";
            const char* WIDE_OPERATORS[] = {
                "++",
                "--",
                "+=",
                "-=",
                "*=",
                "/=",
                "==",
                ">=",
                "<="
            };
            // TODO: place in implementation file so that the namespace is not crowded
            using namespace Utility::String;
            using namespace Common::Error;
            using Common::Token;

            struct LexerState {
                // the code that is being worked on
                std::string code;
                // the current position in the code
                size_t index;

                // the file where the code came from, <stdio> if none were supplied
                std::string filename;

                // the output of the lexer
                std::vector<Common::Token> tokens;
                // any errors when lexing
                std::vector<Common::Error::Error> errors;
            };

            bool StateIsValid(LexerState& state) noexcept {
                // is the state able to be used
                return state.index < state.code.size() && state.code.size() > 0;
            }

            void GetIdentifier(LexerState& state) noexcept {
                
                // capture the start because tokens track that
                size_t start = state.index;

                // the identifier output
                std::ostringstream oss;
                
                while (StateIsValid(state)) {
                    // if the current character is NOT acceptable for identifiers i.e. a-z, A-Z, 0-9 or an underscore
                    if (!(
                            StringContains(ASCII, currentCharacter)
                        ||  StringContains(NUMS, currentCharacter)
                        ||  currentCharacter == '_'
                    )) break;

                    oss << currentCharacter;

                    ++state.index;
                }

                // the state should be left in a way that means that AFTER the index is incremented in the main loop
                // it should then point to the first UNREAD character
                // basically. the function should leave it at the last character used
                --state.index;

                
                Token token;

                token.start = start;
                token.end = state.index;

                // get the string
                std::string view = oss.str();

                // Check whether the string is a value keyword (i.e true/false/null) and set the type accordingly


                std::cout << view.size() << '\n';

                if (view == "true") {
                    // set the type to be a boolean
                    token.type = T_TYPE_BOOLEAN;
                    token.values.bType = true;
                    state.tokens.push_back(token);
                    return;
                } 
                else if (view == "false") {
                    // set the type to be a boolean
                    token.type = T_TYPE_BOOLEAN;
                    token.values.bType = false;
                    state.tokens.push_back(token);
                    return;
                }
                else if (view == "null") {
                    // set the type to be an integer
                    token.type = T_TYPE_INTEGER;
                    token.values.iType = 0;
                    state.tokens.push_back(token);
                    return;
                }



                // the string is just a regular identifier

                token.type = T_TYPE_IDENTIFIER;


                // since tokens strings are only pointers. we need to heap allocate them.
                // otherwise the string will go out of scope and we get a segmentation fault
                char* heapString = new char[view.size()];

                // copy the strings contents to the heap
                memcpy(reinterpret_cast<void*>(heapString), view.data(), view.size() * sizeof(char));

                token.values.sType = heapString;

                state.tokens.push_back(token);
            }

            void GetNumber(LexerState& state) noexcept {
                // the number to be output
                std::ostringstream oss;

                // track the start because tokens require this
                size_t start = state.index;

                // if the first part was a decimal, we need to track it
                size_t decimals = currentCharacter == '.'? 1:0;
                if (decimals > 0) {
                    oss << currentCharacter;
                    ++state.index;
                }


                while (StateIsValid(state)) {
                    // if the number has ended break from the loop
                    if (!StringContains(NUMS, currentCharacter)) break;


                    // if we find a decimal point increase the count
                    if (currentCharacter == '.') ++decimals;
                    if (decimals > 1) {
                        Error err;

                        err.errorID = "L0002";
                        err.errorDesc = "Too many decimals in number literal";
                        err.filename = state.filename;

                        err.code = state.code;

                        err.line = GetLineFromPosition(state.code, state.index);
                        err.collumn = GetCollumnFromPosition(state.code, state.index);

                        err.start = start;
                        err.end = start + 1;

                        err.severityInt = E_SEVERITY_ERROR;
                        err.severityName = E_SEVERITY_NAME_ERROR;

                        state.errors.push_back(err);
                        return;
                    }

                    // add the current character to the string
                    oss << currentCharacter;

                    // get the next character
                    ++state.index;

                }

                /// Convert string to int / float

                // Check the type of the number
                size_t numType = decimals == 0? T_TYPE_INTEGER:T_TYPE_FLOAT;


                if (StateIsValid(state)) {
                    

                    // nothing/i:0, means integer, u:1, means unsigned integer, l:2, means long,
                    // f:3, means float, d:4, means double

                    // Gets the explicit type of number
                    switch (currentCharacter) {
                        case 'i': // integer
                            numType = T_TYPE_INTEGER;
                            break;
                        case 'u': // unsigned integer
                            numType = T_TYPE_UNSIGNED_INTEGER;
                            break;
                        case 'l': // long
                            numType = T_TYPE_LONG;
                            break;
                        case 'f': // float
                            numType = T_TYPE_FLOAT;
                            break;
                        case 'd': // double
                            numType = T_TYPE_DOUBLE;
                            break;
                        default:
                            // we didn't have a suffix. so we should put the index back to where the literal ends
                            --state.index; 
                    }

                    // get the next character
                    // is at the end because otherwise the state can be left invalid if the number is the last character
                    ++state.index;
                }

                // If the number has decimals. we cant use anything other than float and double
                if (decimals > 0 && !(numType == T_TYPE_FLOAT || numType == T_TYPE_DOUBLE)) {
                        Error err;

                        err.errorID = "L0003";
                        err.errorDesc = "Invalid explicit type for number literal that contains decimals";
                        err.filename = state.filename;

                        err.code = state.code;

                        err.line = GetLineFromPosition(state.code, state.index);
                        err.collumn = GetCollumnFromPosition(state.code, state.index);

                        err.start = start;
                        err.end = start + 1;

                        err.severityInt = E_SEVERITY_ERROR;
                        err.severityName = E_SEVERITY_NAME_ERROR;

                        state.errors.push_back(err);
                        return;
                }


                // Create token
                Token token;

                token.type = numType;

                // Convert and set the correct typed value of the token

                // if the number is a decimal and it has a leading or trailing period. std::sto... will throw.
                // so we need to add a zero at the start and at the end. but ONLY if it has decimals in it (otherwise we would change the value)

                std::ostringstream finalNumber;

                if (decimals > 0) finalNumber << '0';
                    finalNumber << oss.str();
                if (decimals > 0) finalNumber << '0';


                switch (numType) {
                    case T_TYPE_INTEGER:
                        token.values.iType = std::stoll(finalNumber.str());
                        break;
                    case T_TYPE_UNSIGNED_INTEGER:
                        token.values.uType = std::stoull(finalNumber.str());
                        break;
                    case T_TYPE_LONG:
                        token.values.iType = std::stoll(finalNumber.str());
                        break;
                    case T_TYPE_UNSIGNED_LONG:
                        token.values.uType = std::stoull(finalNumber.str());
                        break;
                    case T_TYPE_FLOAT:
                        token.values.fType = std::stod(finalNumber.str());
                        break;
                    case T_TYPE_DOUBLE:
                        token.values.fType = std::stoi(finalNumber.str());
                        break;
                }

                token.start = start;
                token.end = state.index;

                state.tokens.push_back(token);


                // the state should be left in a way that means that AFTER the index is incremented in the main loop
                // it should then point to the first UNREAD character
                // basically. the function should leave it at the last character used
                // also without this, suffixes don't work
                --state.index;
            }

            void GetOperator(LexerState& state) noexcept {
                
                size_t start = state.index;

                // get the type of operator
                char operatorValue[2] = {currentCharacter, 0};
                // get the next character

                if (StateIsValid(state)) {
                    // if the operator value is one of the operators that has a two sized type, check for it

                    // get the second character
                    ++state.index;

                    // since the pointer needs to be decremented if it is not wide.
                    // track whether or not we found a wide operator
                    bool found = false;
                    // super jank. test thoughrouly
                    for (size_t i = 0; i < sizeof(WIDE_OPERATORS)/sizeof(const char*); ++i) {

                        if (WIDE_OPERATORS[i][0] == operatorValue[0] && currentCharacter == WIDE_OPERATORS[i][1]){
                            operatorValue[1] = currentCharacter;
                            found = true;
                            break;
                        }
                    }

                    // since we have to leave the output at the last item read
                    // if we didn't read anything at this position
                    // we need to decrement the index by one to put it back to the original position
                    if (!found) --state.index;
                }

                // Create and add token

                Token token;

                token.start = start;
                token.end = state.index;

                token.type = T_TYPE_OPERATOR;

                // since tokens strings are only pointers. we need to heap allocate them.
                // otherwise the string will go out of scope and we get a segmentation fault
                char* heapString = new char[2];

                // copy the strings contents to the heap
                memcpy(reinterpret_cast<void*>(heapString), operatorValue, 2 * sizeof(char));

                token.values.sType = heapString;

                state.tokens.push_back(token);


            }

            int LexCode(LexerState& state) noexcept {

                if (!StateIsValid(state)) return -1;

                state.index = 0;
                state.tokens.clear();
                state.errors.clear();

                while (StateIsValid(state)) {

                    if (StringContains(WHITESPACE, currentCharacter)) {
                        // ignore whitespace.
                        // newlines are handled elsewhere. we don't deal with them in the lexer anymore
                    }
                    else if (StringContains(ASCII, currentCharacter)) {
                        GetIdentifier(state);
                    }
                    else if (StringContains(NUMS, currentCharacter)) {
                        GetNumber(state);
                    }
                    else if (StringContains(OPERATORS, currentCharacter)) {
                        GetOperator(state);
                    }

                    else {

                        Error err;

                        err.errorID = "L0001";
                        err.errorDesc = "Unexpected Character";
                        err.filename = state.filename;

                        err.code = state.code;

                        err.line = GetLineFromPosition(state.code, state.index);
                        err.collumn = GetCollumnFromPosition(state.code, state.index);

                        err.start = state.index;
                        err.end = state.index+1;

                        err.severityInt = E_SEVERITY_ERROR;
                        err.severityName = E_SEVERITY_NAME_ERROR;

                        state.errors.push_back(err);

                    }

                    ++state.index;
                }

                return 0;
            }
        }
    }
}