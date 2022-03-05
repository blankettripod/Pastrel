#pragma once

#include <cstddef>
#include <cstdint>

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