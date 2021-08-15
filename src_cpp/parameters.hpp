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
static const int N_BIN = 12;
static const int N_BIN_MINUS_1 = 11;
static const std::vector<int> BINS = {0, 2, 4, 8, 16, 32, 64, 128, 256, 1024, 2048};
static const int N_INFO = 9;
static int N_HIST = 100;


#endif //SRC_CPP_PARAM_H
