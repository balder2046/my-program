cmake_minimum_required(VERSION 3.6)
project(network)

set(CMAKE_CXX_STANDARD 14)

find_package(Boost REQUIRED COMPONENTS system regex )
set(SOURCE_FILES main.cpp asio_test.cpp)
add_executable(network ${SOURCE_FILES} )
target_link_libraries(network ${Boost_LIBRARIES})