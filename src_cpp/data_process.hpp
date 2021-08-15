#ifndef SRC_CPP_DATA_PROCESS_HPP
#define SRC_CPP_DATA_PROCESS_HPP

#include <iostream>
#include <fstream>
#include <algorithm>
#include <iterator>
#include <vector>
#include <string>
#include <set>
#include "tools.hpp"

class DataProcess {
public:
    static std::vector<int> get_types(const std::string &file_path) {
        std::cout << "get_types" << std::endl;
        std::ifstream fp(file_path);
        std::string s;
        std::getline(fp, s);
        std::set<std::string> type_set{};
        while (!fp.eof()) {
            std::getline(fp, s);
            if (s.empty()) { continue; }
            auto pos1 = s.find(',', 0);
            if (pos1 == std::string::npos) {
                break;
            }
            pos1++;
            auto pos2 = s.find(',', pos1);
            if (pos2 == std::string::npos) {
                break;
            }
            type_set.insert(s.substr(pos1, pos2 - pos1));
        }
        fp.close();
        auto type_list = std::vector<std::string>(type_set.begin(), type_set.end());
        std::vector<int> type_nums{};
        auto get_tail_num = [&](const std::string &s) {
            if (s.empty()) { return -1; }
            auto pos = s.rfind('_');
            if (pos == std::string::npos) { return -1; }
            return std::stoi(s.substr(pos + 1));
        };
        std::for_each(type_list.begin(), type_list.end(), [&](const auto &o) { type_nums.push_back(get_tail_num(o)); });
        std::sort(type_nums.begin(), type_nums.end());
        std::cout << "type_nums: ";
        std::copy(type_nums.begin(), type_nums.end(), std::ostream_iterator<int>(std::cout, ","));
        std::cout << "\n";
        if (type_nums.empty()) {
            std::cout << "Warning: types is empty.\n";
            type_nums.push_back(0);
        }
        return type_nums;
    }

    static bool parse_exception(const std::string &line, std::string &nc_ip, int &exception_type,
                                int &exception_hour, std::string &content) {
        if (line.empty()) { return false; }
        static std::string::size_type i;
        static std::string::size_type j;
        i = line.find(',');
        nc_ip = line.substr(0, i);
        i++;
        j = line.find(',', i);
        exception_type = parse_trail_num(line.substr(i, j - i));
        j++;
        i = line.find(',', j);
        exception_hour = TimeTools::StrToHour21th(line.substr(j, i - j));
        return true;
    }

    static void parse_label(const std::string &line, std::string &nc_ip, int &hour, short &label) {
        static const char c = ',';
        auto pos_i = line.find_first_of(c, 0);
        nc_ip = line.substr(0, pos_i);
        pos_i++;
        auto pos_j = line.find(c, pos_i);
        hour = TimeTools::StrToHour21th(line.substr(pos_i, pos_j - pos_i));
        pos_j++;
        static const char char_true = 'T';
        if (line.length() > pos_j) {
            label = char_true == line[pos_j] ? 1 : 0;
        }
    }

    static int parse_trail_num(const std::string &str) {
        auto pos = str.find_last_of('_');
        if (pos == std::string::npos) { return -1; }
        return std::stoi(str.substr(pos + 1));
    }

    static bool parse_info(const std::string &line, std::string &nc_ip, std::vector<int> &feature) {
        if (line.empty()) {
            return false;
        }
        static const int N_COL = 11;
        static std::vector<int> pos_list(N_COL);
        static std::vector<std::string> col_list(N_COL);
        pos_list.clear();
        col_list.clear();
        for (int i = 0; i < int(line.length()); ++i) {
            if (line[i] == ',') {
                pos_list.push_back(i);
            }
        }
        if (pos_list.empty()) {
            return false;
        }
        col_list.push_back(line.substr(0, pos_list[0]));
        for (int i = 1; i < int(pos_list.size()); ++i) {
            col_list.push_back(line.substr(pos_list[i - 1] + 1, pos_list[i] - pos_list[i - 1] - 1));
        }
        col_list.push_back(line.substr(pos_list.back() + 1));
//        0nc_ip,1physical_model,2cpu_generation_full,3manufacturer,4cluster_alias,
//        5cluster_usage,6mem_pn,7mem_manufacturer,8bios_version,9os_release,
//        10bmc_version
        nc_ip = col_list.front();
        feature.clear();
        static const int N_USEFUL_FEATURE = 9;
        feature.reserve(N_USEFUL_FEATURE);
        for (int i = 1; i < 4; ++i) {
            feature.push_back(parse_trail_num(col_list[i]));
        }
        for (int i = 5; i < N_COL; ++i) {
            feature.push_back(parse_trail_num(col_list[i]));
        }
        return true;
    }
};

#endif //SRC_CPP_DATA_PROCESS_HPP
