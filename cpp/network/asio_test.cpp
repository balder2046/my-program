//
// Created by 赵磊 on 2017/4/26.
//
#include "boost/asio.hpp"
#include "asio_test.h"
#include "string"
#include "iostream"
using namespace boost;

boost::asio::ip::tcp::endpoint EndPointFromIP(std::string ip, unsigned short port, boost::system::error_code &ec)
{

}

int asio_test()
{
    std::string raw_ip_address = "127.0.0.1";
    unsigned short port = 3306;
    system::error_code err;
    asio::ip::address ip_address = asio::ip::address::from_string(raw_ip_address.c_str(),err);
    if (err.value() != 0)
    {
        std::cout << "Failed to parse the address " << raw_ip_address << " errorcode: " << err.value();
        std::cout << " reasion: " << err.message() << std::endl;
        return err.value();
    }
    asio::ip::tcp::endpoint ep(ip_address,port);
    return 0;
}
int connect_test()
{
    std::string raw_ip_address = "127.0.0.1";
    unsigned short port = 8001;
    system::error_code err;
    asio::ip::address ip_address = asio::ip::address::from_string(raw_ip_address.c_str(),err);
    if (err.value() != 0)
    {
        std::cout << "Failed to parse the address " << raw_ip_address << " errorcode: " << err.value();
        std::cout << " reasion: " << err.message() << std::endl;
        return err.value();
    }
    asio::ip::tcp::endpoint ep(ip_address,port);

    // create a io_service
    asio::io_service ios;
    asio::ip::tcp::socket sock(ios,ep.protocol());
    try
    {
        sock.connect(ep);
        std::cout << "Connect OK!";
    }
    catch (system::system_error &err)
    {
        std::cout << "Failed to connect " << err.code() << " reason:" << err.what() << std::endl;
    }
    return 0;

}