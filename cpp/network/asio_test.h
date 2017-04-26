//
// Created by 赵磊 on 2017/4/26.
//

#ifndef NETWORK_ASIO_TEST_H
#define NETWORK_ASIO_TEST_H

#include "string"
#include "boost/asio.hpp"
boost::asio::ip::tcp::endpoint EndPointFromIP(std::string ip, unsigned short port, boost::system::error_code &ec);
int asio_test();
int connect_test();
#endif //NETWORK_ASIO_TEST_H
