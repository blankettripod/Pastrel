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

                // array for whether each value is a node or whether it is a token
                bool *isNode;
                // an array of values pointing to either other nodes or tokens
                union {
                   Node* nType;
                   Token* tType; 
                } *values;

                size_t start;
                size_t end;

            };

        }
    }
}