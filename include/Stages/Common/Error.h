#pragma once

#include <cstddef>
#include <cstdint>

#include <string_view>
#include <sstream>

#define E_SEVERITY_INFO static_cast<size_t>(0)
#define E_SEVERITY_WARNING static_cast<size_t>(1)
#define E_SEVERITY_ERROR static_cast<size_t>(2)
#define E_SEVERITY_FATAL static_cast<size_t>(3)

#define E_SEVERITY_NAME_INFO "Info"
#define E_SEVERITY_NAME_WARNING "Warning"
#define E_SEVERITY_NAME_ERROR "Error"
#define E_SEVERITY_NAME_FATAL "FATAL"

namespace Pastrel {
    namespace Stages {
        namespace Common {
            namespace Error {

                // structure containing information about an error
                struct Error {
                    // the id of the error
                    std::string errorID;
                    // the description of the error
                    std::string errorDesc;
                    // the file where the error occurred
                    std::string filename;

                    // the code of the file
                    std::string code;

                    // the line of the error
                    size_t line;
                    // the collumn of the error
                    size_t collumn;

                    // the starting position 
                    // NOTE: not the same as the collumn as this is the position in the code string
                    //       rather than the position on the current
                    size_t start;

                    // the ending position 
                    // NOTE: not the same as the collumn as this is the position in the code string
                    //       rather than the position on the current
                    size_t end;

                    // the severity of the error (internal, use severityName for printing)
                    size_t severityInt;
                    // the printing severity of the error
                    std::string severityName;
                };

                // create an error string from an error structure
                std::string CreateError(const Error& err) {
                    std::ostringstream oss;

                    // example
                    //          Error                   L0000          at        <stdio>        :       69         :          420
                    oss << err.severityName << ' ' << err.errorID << " at " << err.filename << ':' << err.line << ':' << err.collumn << '\n';
                    
                    //       nice error
                    oss << err.errorDesc << '\n';
                    

                    // if the length of the arrow is either zero or negative
                    // or the string is empty
                    // then return the current message (for use of errors that are not related to code i.e. file io)
                    if ((err.start >= err.end) || (err.code.size() == 0)) return oss.str();

                    oss << err.code << '\n';

                    // for every character before the collumn, put a space
                    for (size_t i = 0; i < err.collumn; ++i) {
                        oss << ' ';
                    }

                    // this is the start of the offending code
                    oss << '^';

                    // this is the offending code. length has one subtracted because of the start carat
                    for (size_t i = 0; i < err.end-err.start - 1; ++i) {
                        oss << '~';
                    }

                    return oss.str();
                }

            }
        }
    }
}