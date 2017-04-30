cmake_minimum_required(VERSION 3.6)
project(network)

set(CMAKE_CXX_STANDARD 14)

find_package(Boost REQUIRED COMPONENTS system regex thread)
set(SOURCE_FILES main.cpp asio_test.cpp)
add_executable(network ${SOURCE_FILES} )
target_link_libraries(network ${Boost_LIBRARIES})

add_executable(client_test client_test.cpp)
target_link_libraries(client_test ${Boost_LIBRARIES})

add_executable(server_test server_test.cpp)
target_link_libraries(server_test ${Boost_LIBRARIES})