#pragma once

#define R_MODIFIER_STOCK 0ul
#define R_MODIFIER_REPEATING 1ul
#define R_MODIFIER_CHOICE 2ul

#define R_TYPE_TYPE 0ul
#define R_TYPE_LITERAL 1ul
#define R_TYPE_RULE 2ul

namespace Pastrel {
    namespace Stages {
        namespace Parser {
            struct Rule {

                typedef struct {
                    size_t type;
                    const char* literal;
                } Value;

                typedef struct {
                    size_t type;
                    size_t modifier;
                    Value values[16]; // is array because choice has to have multiple values
                } Part;


                /*

                needs to be able to check against multiple parts

                needs to be able to check against rules and literals in the same rule
                i.e. parts: rule, rule, literal, rule

                needs to be able to support the folowing part types
                modifier    stock
                modifier    repeating
                modifier    choice
                type        type (token type)
                type        literal (verbatime value)
                type        other rule


                type needs to be able to store up to a size_t
                parts needs to be a vector of part


                repeating rules are declared as normal
                then when a rule that requires a repeat is made 
                the repeating rule is used with the repeating modifier

                */

                // rules should NEVER contain rule structures
                // they should only contain names of other rules
                // this should fix a bug in the previous python version
                // where rules weren't aplying correctly when 
                // more than one rule deep


                size_t type;
                
                // higher prededence means chosen first
                size_t precedence;

    
                Part parts[16];

            };
        }
    }
}