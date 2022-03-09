#pragma once

namespace Pastrel {
    namespace Stages {
        namespace Parser {
            struct Rule {
                /*

                needs to be able to check against multiple parts

                needs to be able to check against rules and literals in the same rule
                i.e. parts: rule, rule, literal, rule

                needs to be able to support the folowing part types
                modifier    repeating
                modifier    choice
                type        literal (verbatime value)
                type        type (token type)
                type        other rule



                type needs to be able to store up to a size_t
                parts needs to be a vector of part


                */

                struct part {

                    size_t type;
                    size_t modifier;

                    union values {
                        Rule* rule;
                        const char* type;
                    };
                };

                std::vector<part> parts;
            };
        }
    }
}