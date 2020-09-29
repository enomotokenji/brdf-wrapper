cmake_minimum_required(VERSION 2.8.12)
project(brdf)

add_subdirectory(pybind11)
pybind11_add_module(brdf brdf.cpp)
target_link_libraries(brdf PRIVATE pybind11::module)
