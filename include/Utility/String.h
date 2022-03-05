#pragma once

#include <cstddef>
#include <cstdint>

#include <sstream>
#include <string>

namespace Pastrel {
    namespace Utility {
        namespace String {

            std::string GetCodeFromLine(const std::string_view code, size_t line) noexcept {
                std::ostringstream oss;

                size_t currentLine = 0;

                for (size_t i = 0; i < code.size(); ++i){

                    // if this is the line we are searching for, add the current character to the string
                    if (currentLine == line) oss << code.at(i);

                    // we are past the line we are searching for. return
                    if (currentLine > line) break;

                    // we have entered a new line
                    //   this is at the end because otherwise if the line is non zero then the string will have a leading newline
                    //   instead of a trailing newline which would mess up printing
                    if (code.at(i) == '\n') ++currentLine;

                }

                return oss.str();

            }

            size_t GetCollumnFromPosition(const std::string_view code, size_t position) noexcept {

                // if the position is greater than the code size then we cant proceed. return the last item
                if (position >= code.size()) return code.size() - 1;

                size_t currentCollumn = 0;
                

                for (size_t i = 0; i < code.size(); ++i) {
                    // increase the current collumn
                    ++currentCollumn;


                    // if this is the position we wanted, return
                    if (i == position) break;

                    // if the character is a newline then set current collumn to 0
                    if (code.at(i) == '\n') {
                        currentCollumn = 0;
                    }


                }

                return currentCollumn - 1;
            }

            size_t GetLineFromPosition(const std::string_view code, size_t position) noexcept {

                // if the position is greater than the code size then we cant proceed. return the last item
                if (position >= code.size()) return code.size() - 1;

                size_t currentIndex = 0;
                size_t currentLine = 0;

                while (currentIndex < position) {
                    if (code.at(currentIndex) == '\n') ++currentLine;
                    ++currentIndex;
                }

                return currentLine;
            }


            // a bunch of functions that check if a string contains a substring

            inline bool StringContains(const std::string_view string, const std::string_view substring) noexcept {
                return string.find(substring) != std::string::npos;
            }

            inline bool StringContains(const std::string_view string, std::initializer_list<std::string_view> substrings) noexcept {
                for (const auto& substring : substrings) {
                    if (string.find(substring) != std::string::npos) return true;
                }
            }

            inline bool StringContains(const std::string_view string, const char* substring) noexcept {
                std::string sstring(substring);
                return string.find(sstring) != std::string::npos;
            }

            inline bool StringContains(const std::string_view string, std::initializer_list<const char*> substrings) noexcept {
                for (const auto& substring : substrings) {
                std::string sstring(substring);
                    if (string.find(sstring) != std::string::npos) return true;
                }
            }

            inline bool StringContains(const std::string_view string, char substring) noexcept {
                return string.find(substring) != std::string::npos;
            }

            inline bool StringContains(const std::string_view string, std::initializer_list<char> substrings) noexcept {
                for (const auto& substring : substrings) {
                    if (string.find(substring) != std::string::npos) return true;
                }
            }

            inline bool StringContains(const char* cstring, const std::string_view substring) noexcept {
                std::string_view string(cstring);
                return string.find(substring) != std::string::npos;
            }

            inline bool StringContains(const char* cstring, std::initializer_list<std::string_view> substrings) noexcept {
                std::string_view string(cstring);
                for (const auto& substring : substrings) {
                    if (string.find(substring) != std::string::npos) return true;
                }
            }

            inline bool StringContains(const char* cstring, const char* substring) noexcept {
                std::string_view string(cstring);
                std::string sstring(substring);
                return string.find(sstring) != std::string::npos;
            }

            inline bool StringContains(const char* cstring, std::initializer_list<const char*> substrings) noexcept {
                std::string_view string(cstring);
                for (const auto& substring : substrings) {
                std::string sstring(substring);
                    if (string.find(sstring) != std::string::npos) return true;
                }
            }

            inline bool StringContains(const char* cstring, char substring) noexcept {
                std::string_view string(cstring);
                return string.find(substring) != std::string::npos;
            }

            inline bool StringContains(const char* cstring, std::initializer_list<char> substrings) noexcept {
                std::string_view string(cstring);
                for (const auto& substring : substrings) {
                    if (string.find(substring) != std::string::npos) return true;
                }
            }

        }
    }
}