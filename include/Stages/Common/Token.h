#pragma once

#include <cstddef>
#include <cstdint>

#define T_TYPE_IDENTIFIER 1ul
#define T_TYPE_INTEGER 2ul
#define T_TYPE_UNSIGNED_INTEGER 3ul
#define T_TYPE_LONG 4ul
#define T_TYPE_UNSIGNED_LONG 5ul
#define T_TYPE_FLOAT 6ul
#define T_TYPE_DOUBLE 7ul
#define T_TYPE_BOOLEAN 8ul
#define T_TYPE_OPERATOR 9ul
#define T_TYPE_STRING 10ul
#define T_TYPE_CHAR 11ul

namespace Pastrel {
    namespace Stages {
        namespace Common {

            struct Token {
                // the integer type of the token
                size_t type;

                union {
                    char cType;
                    size_t uType;
                    int64_t iType;
                    const char* sType;
                    bool bType;
                    long double fType;
                    void* vType;
                } values;

                size_t start;
                size_t end;

            };

        }
    }
}