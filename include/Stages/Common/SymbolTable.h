#pragma once

#include <string>
#include <map>

namespace Pastrel {
    namespace Stages {
        namespace Common {
            
            
            class SymbolTable {
            public:
                struct Entry {
                    // the integer type of the symbol
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
                };

                SymbolTable() noexcept;
                SymbolTable(const SymbolTable&) = delete;
                const SymbolTable& operator=(const SymbolTable&) = delete;

                ~SymbolTable() = default;

                bool AddSymbol(std::string& name, const Entry& entry) noexcept {
                    if (symbols.contains(name)) return false;

                    symbols.insert({name, entry});
                }

                inline bool HasSymbol(std::string& name) noexcept {
                    return symbols.contains(name);
                }

                Entry const * GetSymbol(std::string& name) noexcept {
                    if (symbols.contains(name)) return &symbols.at(name);
                    
                    return nullptr;
                }  


            private:
                std::map<std::string, Entry> symbols;

            };
        
        }
    }
}