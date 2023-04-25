#!/usr/bin/env python3
import socket
import os
import struct
import json


def native_format(data):
    result = {
        "format": "NATIVE",
        "serial_time": 0,
        "serial_size": 0,
        "deserial_time": 0,
    }
    return json.dumps(result)

def xml_format(data):
    result = {
        "format": "XML",
        "serial_time": 0,
        "serial_size": 0,
        "deserial_time": 0,
    }
    return json.dumps(result)

def json_format(data):
    result = {
        "format": "JSON",
        "serial_time": 0,
        "serial_size": 0,
        "deserial_time": 0,
    }
    return json.dumps(result)

def gpb_format(data):
    result = {
        "format": "GPB",
        "serial_time": 0,
        "serial_size": 0,
        "deserial_time": 0,
    }
    return json.dumps(result)

def apache_format(data):
    result = {
        "format": "APACHE",
        "serial_time": 0,
        "serial_size": 0,
        "deserial_time": 0,
    }
    return json.dumps(result)

def yaml_format(data):
    result = {
        "format": "YAML",
        "serial_time": 0,
        "serial_size": 0,
        "deserial_time": 0,
    }
    return json.dumps(result)

def msgpack_format(data):
    result = {
        "format": "MSGPACK",
        "serial_time": 0,
        "serial_size": 0,
        "deserial_time": 0,
    }
    return json.dumps(result)

BUFFER_SIZE = 1024

NAME_TO_METHOD = {
    "NATIVE": native_format,
    "XML": xml_format,
    "JSON": json_format,
    "GPB": gpb_format,
    "APACHE": apache_format,
    "YAML": yaml_format,
    "MSGPACK": msgpack_format,
}

TESTING_DATA = {
    "string": "Hello, world!",
    "array": ["Hello", "From", "Kalmykia", "!"],
    "dictionary": {"negn": 1, "hoir": 2, "gurvn": 3, "dorvn": 4},
    "int_num": 42,
    "float_num": 3.1415,
}


def serialization_time(hostname, data):
    return NAME_TO_METHOD[hostname](data)


if __name__ == "__main__":
    # loading info
    host = os.environ['HOST']
    port = int(os.environ['PORT'])
    multicast_addr = os.environ['MULTICAST_ADDR']

    # socket setting up
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        mreq = struct.pack("4sl", socket.inet_aton(multicast_addr), socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # main logic
        while True:

            # waiting client ping
            bytesAddressPair = s.recvfrom(BUFFER_SIZE)

            # response
            data, address = bytesAddressPair
            s.sendto(str.encode(serialization_time(host, TESTING_DATA)), address)