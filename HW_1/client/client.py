#!/usr/bin/env python3
import socket
import os
import json


FORMAT_NUMBER = 7
BUFFER_SIZE = 1024

def multiple_request_processing():
    host = os.environ["MULTICAST_ADDR"]
    port = int(os.environ["PORT"])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        s.sendto(str.encode("Get all timings"), (host, port))

        response_storage = dict()
        while len(response_storage) < FORMAT_NUMBER:
            data, server = s.recvfrom(BUFFER_SIZE)
            data = json.loads(data.decode())
            response_storage[data["format"]] = (data["serial_time"], data["deserial_time"])
            print(data)


def single_request_processing(query_format):
    host = query_format
    port = int(os.environ['PORT'])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((host, port))
        s.sendto(str.encode("Get {} timing".format(query_format)), (host, port))

        data, server = s.recvfrom(BUFFER_SIZE)
        data = json.loads(data.decode())
        print(data)


if __name__ == "__main__":
    multiple_request_processing()
    print()
    print()
    print()
    single_request_processing("XML")