#pragma once

#include <cstddef>
#include <cstdint>

#include <Stages/Common/Token.h>

namespace Pastrel {
    namespace Stages {
        namespace Common {

            struct Node {
                // the integer type of the Node
                size_t type;
                // an array of values pointing to either other nodes or tokens
                struct part {
                    size_t type;
                    union pointers {
                        Node* node;
                        Token* token;
                    };
                };

                std::vector<part> parts;

                size_t start;
                size_t end;
            };

            // common node is used in the parsing stack because both tokens and nodes can be present in the same space
            // also because I cant be bothered to used inheritence as it is messy when using structs
            struct CommonNode {
                size_t type; // 0 = node, 1 = token
                union {
                    Node* node;
                    Token* token;
                } values;
            }; 

        }
    }
}