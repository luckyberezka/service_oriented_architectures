#!/usr/bin/env python3
import socket
import os
import json
import socketserver
import os


FORMAT_NUMBER = 7
BUFFER_SIZE = 1024

HTTP = 'HTTP/1.1'
MB = 1024 ** 2

PROXY_HOST = "0.0.0.0"
PROXY_PORT = 2000

FORMAT_LIST = ["NATIVE", "XML", "JSON", "GPB", "APACHE", "YAML", "MSGPACK"]


def multiple_request_processing():
    host = os.environ["MULTICAST_ADDR"]
    port = int(os.environ["PORT"])

    result_str = ""

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        s.sendto(str.encode("Get all timings"), (host, port))

        response_storage = dict()
        while len(response_storage) < FORMAT_NUMBER:
            data, server = s.recvfrom(BUFFER_SIZE)
            data = json.loads(data.decode())
            response_storage[data["format"]] = (data["serial_time"], data["serial_size"], data["deserial_time"])
            print(data)

            result_part = "{} - {}ms - {} - {}ms\n".format(
                data["format"],
                data["serial_time"] * 1000,
                data["serial_size"],
                data["deserial_time"] * 1000
            )

            result_str += result_part
    return result_str


def single_request_processing(query_format):
    host = query_format
    port = int(os.environ['PORT'])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((host, port))
        s.sendto(str.encode("Get {} timing".format(query_format)), (host, port))

        data, server = s.recvfrom(BUFFER_SIZE)
        data = json.loads(data.decode())
        print(data)

        result_str = "{} - {}ms - {} - {}ms\n".format(
            data["format"],
            data["serial_time"] * 1000,
            data["serial_size"],
            data["deserial_time"] * 1000
        )
    return result_str



class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        data = (data.decode()).split()

        print("Request data {}\n".format(data))

        if len(data) < 2 or data[0] != "get_result":
            response = "Invalid command!\n"
        elif data[1].upper() == "ALL":
            response = multiple_request_processing()
        elif data[1].upper() != "ALL" and data[1].upper() not in FORMAT_LIST:
            response = "Invalid format!\n"
        else:
            response = single_request_processing(data[1].upper())


        socket.sendto(str.encode(response), self.client_address)



if __name__ == "__main__":
    with socketserver.UDPServer((PROXY_HOST, PROXY_PORT), MyUDPHandler) as server:
        print("Running server...")
        server.serve_forever()