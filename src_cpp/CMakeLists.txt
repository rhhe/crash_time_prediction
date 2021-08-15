cmake_minimum_required(VERSION 3.17)
project(src_cpp)

set(CMAKE_CXX_STANDARD 14)

add_executable(src_cpp main.cpp data_process.hpp parameters.hpp tools.hpp feature.hpp)