cmake_minimum_required(VERSION 3.10)

project(cpilot)

set(CMAKE_CXX_STANDARD 14)

add_executable(cpilot main.cpp cpilot.cpp)

install(TARGETS cpilot RUNTIME DESTINATION bin)

