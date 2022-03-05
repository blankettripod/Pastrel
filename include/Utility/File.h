#pragma once

#include <fstream>
#include <sstream>

namespace Pastrel {
    namespace Utility {
        namespace File {
            
            std::string ReadFile(const char* filename) noexcept {
                std::ifstream file;

                std::ostringstream contents;

                file.open(filename);
                if (!file.is_open()) return contents.str();


                std::string line;

                while ( getline(file, line)) {
                    contents << line << '\n';
                }

                file.close();

                return contents.str();

            }

            


        }
    }
}