#!/usr/bin/env python3
import socket
import os
import struct
import json
import timeit
import sys
import xmltodict
import dicttoxml
import yaml
import msgpack
import io
import fastavro
import pickle

import extra_pb2


TESTING_DATA = {
    "string": "Hello, world!",
    "array": [15, 8, 12, 5],
    "dictionary": {"negn": 1, "hoir": 2, "gurvn": 3, "dorvn": 4},
    "int_num": 42,
    "float_num": 3.1415,
}

CURRENT_SERIAL_TESTING_DATA = None

SCHEMA_RECORD = {
    "name": "exmpl",
    "type": 'record',
    "fields": [
        {"name": "string", "type": "string"},
        {"name": "array", "type": {"type": "array", "items": "int"}},
        {"name": "dictionary", "type": {"type": "map", "values": "int"}},
        {"name": "int_num", "type": "int"},
        {"name": "float_num", "type": "float"},
    ]
}

MSG = extra_pb2.Data()

def native_format(extra):
    global TESTING_DATA
    global CURRENT_SERIAL_TESTING_DATA

    TESTING_DATA = extra
    CURRENT_SERIAL_TESTING_DATA = pickle.dumps(TESTING_DATA)

    serial_executor = "pickle.dumps(TESTING_DATA)"
    serial_time = timeit.timeit(stmt=serial_executor, number=1000, globals=globals())

    print("pickle")

    deserial_executor = "pickle.loads(CURRENT_SERIAL_TESTING_DATA)"
    deserial_time = timeit.timeit(stmt=deserial_executor, number=1000, globals=globals())

    result = {
        "format": "NATIVE",
        "serial_time": serial_time,
        "serial_size": sys.getsizeof(CURRENT_SERIAL_TESTING_DATA),
        "deserial_time": deserial_time,
    }
    return json.dumps(result)

def xml_format(extra):

    global TESTING_DATA
    global CURRENT_SERIAL_TESTING_DATA

    TESTING_DATA = extra
    CURRENT_SERIAL_TESTING_DATA = dicttoxml.dicttoxml(TESTING_DATA)

    serial_executor = "dicttoxml.dicttoxml(TESTING_DATA)"
    serial_time = timeit.timeit(stmt=serial_executor, number=1000, globals=globals())

    deserial_executor = "xmltodict.parse(CURRENT_SERIAL_TESTING_DATA)"
    deserial_time = timeit.timeit(stmt=deserial_executor, number=1000, globals=globals())

    result = {
        "format": "XML",
        "serial_time": serial_time,
        "serial_size": sys.getsizeof(CURRENT_SERIAL_TESTING_DATA),
        "deserial_time": deserial_time,
    }
    return json.dumps(result)

def json_format(extra):

    global TESTING_DATA
    global CURRENT_SERIAL_TESTING_DATA

    TESTING_DATA = extra
    CURRENT_SERIAL_TESTING_DATA = json.dumps(TESTING_DATA)

    serial_executor = "json.dumps(TESTING_DATA)"
    serial_time = timeit.timeit(stmt=serial_executor, number=1000, globals=globals())

    deserial_executor = "json.loads(CURRENT_SERIAL_TESTING_DATA)"
    deserial_time = timeit.timeit(stmt=deserial_executor, number=1000, globals=globals())

    result = {
        "format": "JSON",
        "serial_time": serial_time,
        "serial_size": sys.getsizeof(CURRENT_SERIAL_TESTING_DATA),
        "deserial_time": deserial_time,
    }
    return json.dumps(result)

def gpb_format(extra):

    global TESTING_DATA
    global CURRENT_SERIAL_TESTING_DATA
    global MSG

    TESTING_DATA = extra

    MSG = extra_pb2.Data()
    MSG.string = TESTING_DATA["string"]
    MSG.int_num = TESTING_DATA["int_num"]
    MSG.float_num = TESTING_DATA["float_num"]
    MSG.array.extend(TESTING_DATA["array"])
    for key in TESTING_DATA["dictionary"]:
        MSG.dictionary[key] = TESTING_DATA["dictionary"][key]

    CURRENT_SERIAL_TESTING_DATA = MSG.SerializeToString()

    serial_executor = "MSG.SerializeToString()"
    serial_time = timeit.timeit(stmt=serial_executor, number=1000, globals=globals())

    deserial_executor = "MSG.ParseFromString(CURRENT_SERIAL_TESTING_DATA)"
    deserial_time = timeit.timeit(stmt=deserial_executor, number=1000, globals=globals())

    result = {
        "format": "GPB",
        "serial_time": serial_time,
        "serial_size": sys.getsizeof(CURRENT_SERIAL_TESTING_DATA),
        "deserial_time": deserial_time,
    }
    return json.dumps(result)


def apache_format(extra):

    global TESTING_DATA
    global CURRENT_SERIAL_TESTING_DATA

    TESTING_DATA = extra

    wb = io.BytesIO()
    fastavro.schemaless_writer(wb, SCHEMA_RECORD, TESTING_DATA)
    CURRENT_SERIAL_TESTING_DATA = wb.getvalue()

    serial_executor = '''
wb = io.BytesIO()
fastavro.schemaless_writer(wb, SCHEMA_RECORD, TESTING_DATA)
wb.getvalue()
'''
    serial_time = timeit.timeit(stmt=serial_executor, number=1000, globals=globals())

    deserial_executor = '''
wb = io.BytesIO()
wb.write(CURRENT_SERIAL_TESTING_DATA)
wb.seek(0)
fastavro.schemaless_reader(wb, SCHEMA_RECORD)
'''
    deserial_time = timeit.timeit(stmt=deserial_executor, number=1000, globals=globals())

    result = {
        "format": "APACHE",
        "serial_time": serial_time,
        "serial_size": sys.getsizeof(CURRENT_SERIAL_TESTING_DATA),
        "deserial_time": deserial_time,
    }
    return json.dumps(result)

def yaml_format(extra):

    global TESTING_DATA
    global CURRENT_SERIAL_TESTING_DATA

    TESTING_DATA = extra
    CURRENT_SERIAL_TESTING_DATA = yaml.dump(TESTING_DATA)

    serial_executor = "yaml.dump(TESTING_DATA)"
    serial_time = timeit.timeit(stmt=serial_executor, number=1000, globals=globals())

    deserial_executor = "yaml.load(CURRENT_SERIAL_TESTING_DATA, yaml.FullLoader)"
    deserial_time = timeit.timeit(stmt=deserial_executor, number=1000, globals=globals())


    result = {
        "format": "YAML",
        "serial_time": serial_time,
        "serial_size": sys.getsizeof(CURRENT_SERIAL_TESTING_DATA),
        "deserial_time": deserial_time,
    }
    return json.dumps(result)

def msgpack_format(extra):

    global TESTING_DATA
    global CURRENT_SERIAL_TESTING_DATA

    TESTING_DATA = extra
    CURRENT_SERIAL_TESTING_DATA = msgpack.packb(TESTING_DATA)

    serial_executor = "msgpack.packb(TESTING_DATA)"
    serial_time = timeit.timeit(stmt=serial_executor, number=1000, globals=globals())

    deserial_executor = "msgpack.unpackb(CURRENT_SERIAL_TESTING_DATA)"
    deserial_time = timeit.timeit(stmt=deserial_executor, number=1000, globals=globals())


    result = {
        "format": "MSGPACK",
        "serial_time": serial_time,
        "serial_size": sys.getsizeof(CURRENT_SERIAL_TESTING_DATA),
        "deserial_time": deserial_time,
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