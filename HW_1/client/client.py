#!/usr/bin/env python3
import socket
import sys
import os

if __name__ == "__main__":
    SERIALIZATION_FORMAT = 'JSON'
    HOST = "native"
    PORT = 4001

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((HOST, PORT))
        s.sendto(str.encode("Hello UDP Server"), (HOST, PORT))

        msgFromServer = s.recvfrom(1024)

        msg = "Message from Server {}".format(msgFromServer[0])

        print(msg)

        HOST = "json"
        PORT = 4002

        s.connect((HOST, PORT))
        s.sendto(str.encode("Hello UDP Server"), (HOST, PORT))

        msgFromServer = s.recvfrom(1024)

        msg = "Message from Server {}".format(msgFromServer[0])

        print(msg)

