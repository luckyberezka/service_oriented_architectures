#!/usr/bin/env python3
import socket
import sys
import os

def query_processing(query_format):
    host = query_format
    port = int(os.environ['{}_PORT'.format(query_format)])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((host, port))
        s.sendto(str.encode("Hello UDP Server from"), (host, port))

        msgFromServer = s.recvfrom(1024)

        msg = "Message from Server {}".format(msgFromServer[0])

        print(msg)


if __name__ == "__main__":
    query_processing("NATIVE")
    query_processing("JSON")
    query_processing("XML")
    query_processing("GPB")
    query_processing("APACHE")
    query_processing("YAML")
    query_processing("MSGPACK")