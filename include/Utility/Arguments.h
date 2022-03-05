#include <algorithm>
#include <string>

namespace Pastrel {
    namespace Utility {
        namespace Arguments {
            char* getCmdOption(char ** begin, char ** end, const std::string & option) noexcept
            {
                // get all occurences of the option
                char ** itr = std::find(begin, end, option);

                // is the iterator at the end (not found) OR is the iterator the last item (there is no value after)
                if (itr != end && ++itr != end)
                {
                    // returns the first time the option appeared
                    return *itr;
                }
                return 0;
            }

            bool cmdOptionExists(char** begin, char** end, const std::string& option) noexcept
            {
                return std::find(begin, end, option) != end;
            }
        }
    }
}