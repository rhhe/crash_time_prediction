#ifndef SRC_CPP_FEATURE_HPP
#define SRC_CPP_FEATURE_HPP

#include <iostream>
#include <fstream>
#include <algorithm>
#include <iterator>
#include <vector>
#include <string>
#include <set>
#include <sstream>
#include <iterator>

#include "parameters.hpp"
#include "data_process.hpp"


class Feature {
public:
    std::string nc_ip{};
    int sample_hour = 0;
    short label = -1;
    std::vector<int> hist{};
    std::vector<int> info;
public:
    Feature() {
        hist.clear();
        hist.resize(N_BIN * N_HIST, 0);
        info.resize(N_INFO, -1);
    }

    void Fill(const int &except_type, const int &except_hour_minus_sample_hour) {
        if (except_type < 0 || except_type >= N_HIST) { return; }
        if (except_hour_minus_sample_hour < BINS_FRONT) { return; }
        if (except_hour_minus_sample_hour >= BINS_BACK) {
            hist[except_type * N_BIN + N_BIN_MINUS_1]++;
            return;
        }
        i = 0, j = N_BIN_MINUS_1;
        while (j - i > 1) {
            mid = (i + j) / 2;
            if (except_hour_minus_sample_hour < BINS[mid]) {
                j = mid;
            } else { i = mid; }
        }
        hist[except_type * N_BIN + i]++;
    }

    static std::string ToCsvHead() {
        std::stringstream ss;
        ss << "label" << ","
           << "nc_ip" << ","
           << "physical_model" << ","
           << "cpu_generation_full" << ","
           << "manufacturer" << ","
           << "cluster_usage" << ","
           << "mem_pn" << ","
           << "mem_manufacturer" << ","
           << "bios_version" << ","
           << "os_release" << ","
           << "bmc_version" << ",";
        for (int i_hist = 0; i_hist < N_HIST; ++i_hist) {
            for (int i_bin = 0; i_bin < N_BIN; ++i_bin) {
                ss << "h" << i_hist << "b" << i_bin << ",";
            }
        }
        return ss.str().substr(0, ss.str().length() - 1);
    }

    std::string ToCsvLine() const {
        std::stringstream ss;
        ss << label << ","
           << nc_ip << ",";
        std::copy(info.begin(), info.end(), std::ostream_iterator<int>(ss, ","));
        std::copy(hist.begin(), hist.end(), std::ostream_iterator<int>(ss, ","));
        return ss.str().substr(0, ss.str().length() - 1);
    }


private:
    int i = 0;
    int j = 0;
    int mid = 0;
};

class FeatureMaker {
protected:
    std::vector<Feature> features;
    std::unordered_map<std::string, std::vector<int>> ip_to_iFeatures_mapper{};
    std::unordered_map<std::string, std::vector<std::vector<int>>> ip_to_exception_hour_mapper{};

public:
    //! read data -> train data -> exception -> types
    static void UpdateNHistWithExceptionFile(const std::string &fn = FILE_TEST_EXCEPTION) {
        std::cout << "UpdateNHistWithExceptionFile: " << fn << std::endl;
        auto type_nums = DataProcess::get_types(fn);
        N_HIST = *std::max_element(type_nums.begin(), type_nums.end()) + 1;
    }

    //! read data -> train data -> sample label -> feature instances
    void ReadLabel(const std::string &label_file) {
        std::cout << "read sample data: " << label_file << std::endl;
        std::ifstream fp_label(label_file);
        if (!fp_label) {
            std::cout << "open file failed: " << label_file << std::endl;
            throw std::runtime_error("open file failed: " + label_file);
        }
        std::string line{};
        std::getline(fp_label, line);
        std::cout << line << std::endl;
        while (!fp_label.eof()) {
//            std::cout << "line: " << line << std::endl;
            std::getline(fp_label, line);
            if (line.empty()) { break; }
            features.emplace_back();
            auto &f = features.back();
            DataProcess::parse_label(line, f.nc_ip, f.sample_hour, f.label);
//            std::cout << f.nc_ip << "~" << f.sample_hour << "~" << f.label << std::endl;
        }
        fp_label.close();
    };

    //! read data -> train data -> sample label -> feature instances
    void ReadLabelWithLessFalseLabel(const std::string &label_file) {
        std::cout << "read sample data: " << label_file << std::endl;
        std::ifstream fp_label(label_file);
        if (!fp_label) {
            std::cout << "open file failed: " << label_file << std::endl;
            throw std::runtime_error("open file failed: " + label_file);
        }
        std::string line{};
        std::getline(fp_label, line);
        std::cout << line << std::endl;
        Feature f;
        int i_false = 0;
        while (!fp_label.eof()) {
//            std::cout << "line: " << line << std::endl;
            std::getline(fp_label, line);
            if (line.empty()) { break; }
            DataProcess::parse_label(line, f.nc_ip, f.sample_hour, f.label);
//            std::cout << f.nc_ip << "~" << f.sample_hour << "~" << f.label << std::endl;
            if (f.label == 0) {
                if ((i_false % 500) == 0) {
                    features.push_back(f);
                }
            } else {
                features.push_back(f);
            }
            i_false++;
        }
        fp_label.close();
    };

    //! feature instances -> nc_ip to i_feature_list mapper
    void MakeIpToFeaturesMapper() {
        std::cout << "make ip-to-iFeatures mapper." << std::endl;
        for (int i_f = 0; i_f < int(features.size()); ++i_f) {
            const auto &k = features.at(i_f).nc_ip;
            if (ip_to_iFeatures_mapper.find(k) == ip_to_iFeatures_mapper.end()) {
                ip_to_iFeatures_mapper[k] = std::vector<int>(0);
            }
            ip_to_iFeatures_mapper[k].push_back(i_f);
        }
    }

    void MakeIpToHourListMapper() {
        std::vector<std::string> ip_list{};
        std::for_each(features.begin(), features.end(), [&](const Feature &f) { ip_list.push_back(f.nc_ip); });
        std::sort(ip_list.begin(), ip_list.end());
        for (const auto &ip: ip_list) {
            ip_to_exception_hour_mapper[ip].resize(N_HIST, {});
        }
    }

    //! read data -> train data -> nc info -> add to feature instances
    void ReadNCInfo(const std::string &file_name_nc_info) {
        std::cout << "read nc infos." << std::endl;
        std::ifstream fp_train_info(file_name_nc_info);
        if (!fp_train_info) {
            std::cout << "open file failed: " << file_name_nc_info << std::endl;
            throw std::runtime_error("open file failed: " + file_name_nc_info);
        }
        std::string line{};
        std::getline(fp_train_info, line);
        std::cout << line << std::endl;
        std::string nc_ip{};
        std::vector<int> info_features;
        while (!fp_train_info.eof()) {
            std::getline(fp_train_info, line);
//            std::cout << "line: " << line << std::endl;
            if (line.empty()) { break; }
            if (!DataProcess::parse_info(line, nc_ip, info_features)) { continue; }
//            std::cout << nc_ip << "~";
//            std::copy(info_features.begin(), info_features.end(), std::ostream_iterator<int>(std::cout, "~"));
//            std::cout << std::endl;
            auto iter = ip_to_iFeatures_mapper.find(nc_ip);
            if (iter == ip_to_iFeatures_mapper.end()) { continue; }
            for (const auto i_f : iter->second) {
                features[i_f].info = info_features;
            }
        }
        fp_train_info.close();
    }

    //! read data -> exception data -> record hour info
    void FillExceptionInfo(const std::string &file_name_exception) {
        std::cout << "FillExceptionInfo" << std::endl;
        std::ifstream fp_train_exception(file_name_exception);
        if (!fp_train_exception) {
            std::cout << "open file failed: " << file_name_exception << std::endl;
            throw std::runtime_error("open file failed: " + file_name_exception);
        }
        std::string line{};
        std::string nc_ip{};
        std::getline(fp_train_exception, line);
        int exception_type;
        int exception_hour;
        std::string content{};
        int i_row = 0;
        while (!fp_train_exception.eof()) {
            if ((i_row % 10000) == 0) { std::cout << "fp_exception: " << i_row << std::endl; }
            i_row++;
            std::getline(fp_train_exception, line);
            if (line.empty()) { break; }
            if (!DataProcess::parse_exception(line, nc_ip, exception_type, exception_hour, content)) { continue; }
            ip_to_exception_hour_mapper[nc_ip].at(exception_type).push_back(exception_hour);
        }
        fp_train_exception.close();
    }

    //! read data -> train data -> exception data -> fill into feature
    void FillExceptionInfoHist(const std::string &file_name_exception) {
        std::cout << "fill data exception into histograms." << std::endl;
        std::ifstream fp_train_exception(file_name_exception);
        if (!fp_train_exception) {
            std::cout << "open file failed: " << file_name_exception << std::endl;
            throw std::runtime_error("open file failed: " + file_name_exception);
        }
        std::string line{};
        std::string nc_ip{};
        std::getline(fp_train_exception, line);
        int exception_type;
        int exception_hour;
        std::string content{};
        int i_row = 0;
        while (!fp_train_exception.eof()) {
            if ((i_row % 10000) == 0) { std::cout << "fp_exception: " << i_row << std::endl; }
            i_row++;
            std::getline(fp_train_exception, line);
//            std::cout << line << std::endl;
            if (line.empty()) { break; }
            if (!DataProcess::parse_exception(line, nc_ip, exception_type, exception_hour, content)) { continue; }
//            std::cout << nc_ip << "," << exception_type << "," << exception_hour << std::endl;
            auto iter = ip_to_iFeatures_mapper.find(nc_ip);
            if (iter == ip_to_iFeatures_mapper.end()) { continue; }
            for (const auto &i_f : iter->second) {
                features[i_f].Fill(exception_type, exception_hour - features[i_f].sample_hour);
            }
        }
        fp_train_exception.close();
    }

    //! write data -> train data -> label + features.
    void WriteToFile(const std::string &file_name) {
        std::cout << "write features to file: " << file_name << "." << std::endl;
        std::ofstream fp_out(file_name);
        fp_out << Feature::ToCsvHead() << std::endl;
        for (const auto &f: features) {
            fp_out << f.ToCsvLine() << std::endl;
        }
        fp_out.close();
    }

    static void make_train_feature() {
        FeatureMaker featureMaker;
//        FeatureMaker::UpdateNHistWithExceptionFile();
        featureMaker.ReadLabelWithLessFalseLabel(FILE_TRAIN_LABEL);
        featureMaker.MakeIpToFeaturesMapper();
        featureMaker.ReadNCInfo(FILE_TRAIN_INFO);
        featureMaker.FillExceptionInfoHist(FILE_TRAIN_EXCEPTION);
        featureMaker.WriteToFile(FILE_TRAIN_FEATURE);
    }

    static void make_test_ip_to_exception_hours() {
        FeatureMaker featureMaker;
        featureMaker.ReadLabel(FILE_TEST_LABEL);
        featureMaker.MakeIpToHourListMapper();
        featureMaker.ReadNCInfo(FILE_TEST_INFO);
        featureMaker.FillExceptionInfo(FILE_TEST_EXCEPTION);
        featureMaker.WriteToFile(FILE_TEST_FEATURE);
    }
};

#endif //SRC_CPP_FEATURE_HPP
