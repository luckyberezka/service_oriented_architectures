#!/usr/bin/env python3
import socket
import sys
import os


if __name__ == "__main__":

    HOST = os.environ['HOST']
    PORT = int(os.environ['PORT'])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        while True:
            bytesAddressPair = s.recvfrom(1024)

            message = bytesAddressPair[0]

            address = bytesAddressPair[1]

            clientMsg = "Message from Client:{}".format(message)
            clientIP = "Client IP Address:{}".format(address)

            print(clientMsg)
            print(clientIP)

            # Sending a reply to client

            s.sendto(str.encode("Hello {} Client".format(HOST)), address)