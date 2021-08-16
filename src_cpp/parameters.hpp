#ifndef SRC_CPP_PARAM_H
#define SRC_CPP_PARAM_H

#include <iostream>
#include <fstream>
#include <algorithm>
#include <iterator>
#include <vector>
#include <string>
#include <set>

static const std::string DIR_DATA = "../../../20210705/data";
static const std::string FILE_TRAIN_EXCEPTION = DIR_DATA + "/train/nc_exceptions.csv";
static const std::string FILE_TRAIN_LABEL = DIR_DATA + "/train/nc_sample_label.csv";
static const std::string FILE_TRAIN_INFO = DIR_DATA + "/train/nc_info.csv";
static const std::string FILE_TRAIN_FEATURE = DIR_DATA + "/feature_train_v2.csv";
static const std::string FILE_TEST_EXCEPTION = DIR_DATA + "/test/nc_exceptions.csv";
static const std::string FILE_TEST_LABEL = DIR_DATA + "/test/nc_sample_label.csv";
static const std::string FILE_TEST_INFO = DIR_DATA + "/test/nc_info.csv";
static const std::string FILE_TEST_FEATURE = DIR_DATA + "/feature_test_v2.csv";
static const int N_BIN = 13;
static const int N_BIN_MINUS_1 = 12;
static const int BIN_WIDTH = 4;
static const std::vector<int> BINS = {0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48};
static const int BINS_FRONT = 0;
static const int BINS_BACK = 48;
static const int N_INFO = 9;
static int N_HIST = 70;


#endif //SRC_CPP_PARAM_H
