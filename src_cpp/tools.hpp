#ifndef SRC_CPP_TOOLS_HPP
#define SRC_CPP_TOOLS_HPP

#include <iostream>
#include <fstream>
#include <algorithm>
#include <iterator>
#include <vector>
#include <string>
#include <set>

class TimeTools {
public:
    static int StrToHour21th(const std::string &str) {
        if (str.empty()) { return 0; }
        static int hour_21th_begin = StrToHour("2000-01-01 00:00:00");
        return StrToHour(str) - hour_21th_begin;
    }

protected:
    static int StrToHour(const std::string &str) {
        tm tm_{};
        static const std::string time_format = "%Y-%m-%d %H:%M:%S";
        strptime(str.c_str(), time_format.c_str(), &tm_);
        return int(mktime(&tm_) / 3600);
    }
};

#endif //SRC_CPP_TOOLS_HPP
