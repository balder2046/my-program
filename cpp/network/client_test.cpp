//
// Created by 赵磊 on 2017/4/29.
//
#include <iostream>
#include <strstream>
#include "glog/logging.h"
#include "boost/asio.hpp"
#include "vector"
#include <memory>
#include <functional>
#include <boost/thread.hpp>

using namespace boost::asio;
using namespace boost::system;
using namespace boost;
typedef unsigned long DWORD;
unsigned short g_port = 10001;

void timeout_handler(const boost::system::error_code &ec) {
    if (ec.value())
        std::cout << ec.value() << "   " << ec.message() << std::endl;
}

void connect_handler1(int info, const boost::system::error_code &ec) {
    if (ec.value() != 0) {
        std::cout << "Connection Fail!!!!  ";
        std::cout << ec.value() << "   " << ec.message() << std::endl;
    } else {
        std::cout << "Connection OK! Now Close!!!!" << std::endl;

        std::cout << info;


    }


}

void connect_handler(ip::tcp::socket *socket, const boost::system::error_code &ec) {
    if (ec.value() != 0) {
        std::cout << "Connection Fail!!!!  ";
        std::cout << ec.value() << "   " << ec.message() << std::endl;
    } else {
        std::cout << "Connection OK! " << std::endl;

    }


}


int main() {
    io_service service;
    /*
    boost::asio::deadline_timer timer(service,boost::posix_time::seconds(5));
    cout << "start" << endl;
    timer.async_wait(timeout_handler);
    */




    try {
        ip::address address = ip::address::from_string("127.0.0.1");
        ip::tcp::endpoint ep(address, g_port);
        ip::tcp::socket sock(service, ep.protocol());
        thread::sleep(boost::get_system_time() + boost::posix_time::seconds(3));
        sock.async_connect(ep, std::bind(::connect_handler, &sock, std::placeholders::_1));
        //sock.async_connect(ep, std::bind(::connect_handler1, 5, std::placeholders::_1));


        service.run();
        std::cout << "ok!!!!" << std::endl;
        ip::tcp::socket::send_buffer_size buffer_size;
        sock.get_option(buffer_size);
        std::cout << "the send buffer size is " << buffer_size.value() << std::endl;
        char *buf = new char[1024 * 1024 * 10];
        for (int i = 0; i < 10; ++i) {
            sock.async_write_some(buffer(buf, 1024 * 1024),
                                  [i](const boost::system::error_code &ec, std::size_t bytes) {
                                      std::cout << "send " << bytes << " bytes" << i << std::endl;
                                  });

            //  std::cout << "send " << nsize << " bytes" << std::endl;
        }

        delete[]buf;

    }
    catch (system_error &err) {
        std::cout << "error code: " << err.code() << " reason: " << err.what() << std::endl;
    }


    std::cout << "print any key to exit!!!!";
    getchar();
    return 0;
}


