#!/usr/bin/env python3
import socket
import os
import struct


BUFFER_SIZE = 1024

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
            s.sendto(str.encode("{} ACK".format(host)), address)