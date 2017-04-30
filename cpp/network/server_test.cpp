//
// Created by 赵磊 on 2017/4/29.
//

#include <iostream>
#include <strstream>

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

#define MAX_CLIENT_BUFFER (8192 * 16)

void timeout_handler(const boost::system::error_code &ec) {
    if (ec.value())
        std::cout << ec.value() << "   " << ec.message() << std::endl;
    std::cout << "time handler !!!!!" << std::endl;
}

class client_session {
public:
    client_session(io_service &ios) : socket(ios) {
        total_size = 0;



        //socket.set_option(receivesize);
    }

    ip::tcp::socket socket;
    std::array<char, MAX_CLIENT_BUFFER> buffer_;

    void onReadSome(const error_code &ec, std::size_t bytesread) {
        if (ec.value()) {
            std::cout << "error " << ec.value() << " reason: " << ec.message() << std::endl;
        }
        if (bytesread == 0) {
            onDisconnect();
        } else {
            total_size += bytesread;
            // receve some bytes;
            std::cout << "read " << bytesread << " bytes!" << "total : " << total_size << std::endl;
            read_some_bytes();
        }
    }

    void start() {
        read_some_bytes();
    }

    void read_some_bytes() {
        socket.async_read_some(buffer(buffer_), std::bind(&client_session::onReadSome, this, std::placeholders::_1,
                                                          std::placeholders::_2));
    }

    void onConnect() {
        std::cout << "client connected !!!" << std::endl;
        //  ip::tcp::socket::receive_buffer_size receivesize(10240);
        //   socket.get_option(receivesize);
        //  std::cout << "the receive buffer size is " << receivesize.value() << std::endl;
        start();
    }

    void onDisconnect() {
        std::cout << "client disconnected !!!" << std::endl;
    }

    void Disconnect() {

    }

    int total_size;
};


void client_session_thread(io_service &service) {
    std::cout << "START THREAD" << std::endl;

    //     A a;
    boost::asio::io_service::work work(service);
    service.run();

}

void client_session_thread1(io_service &service) {
    std::cout << "START THREAD" << std::endl;
    while (true) {
        //     A a;
        boost::asio::deadline_timer timer(service);
        timer.expires_from_now(boost::posix_time::seconds(5));
        timer.async_wait(timeout_handler);
        service.run();
        service.reset();
        //  std::cout << "print server::run" << std::endl;
        //    a.print();
    }

}

void listen_server() {
    io_service service;
    boost::thread clientthread(std::bind(client_session_thread, std::ref(service)));
    ip::address bindaddress = ip::address_v4::any();
    ip::tcp::endpoint ep = ip::tcp::endpoint(ip::address_v4::any(), g_port);
    ip::tcp::acceptor acceptor = ip::tcp::acceptor(service);
    error_code errcode;
    acceptor.open(ep.protocol(), errcode);
    std::vector<std::unique_ptr<client_session> > sessions;
    if (errcode.value() != 0) {
        std::cout << errcode.message() << std::endl;
        return;
    }
    acceptor.bind(ep, errcode);
    if (errcode.value() != 0) {
        std::cout << errcode.message() << std::endl;
        return;
    }
    acceptor.listen(20);
    std::cout << "Server start listening!! " << std::endl;
    int index = 0;
    for (int i = 0; i < 20; ++i) {
        std::unique_ptr<client_session> newsession(new client_session(service));
        acceptor.accept(newsession->socket);

        newsession->onConnect();
        sessions.push_back(std::move(newsession));
        index++;
        std::cout << "Accept connection " << index << std::endl;


    }
}

int main() {
    io_service service;

    //boost::asio::deadline_timer timer(service,boost::posix_time::seconds(5));
    //cout << "start" << endl;
    //timer.async_wait(timeout_handler);

    boost::thread serverthread(listen_server);
    serverthread.join();

    getchar();
    return 0;
}

