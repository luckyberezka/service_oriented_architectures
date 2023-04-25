import socket
import struct
from sys import argv

HOST = "0.0.0.0"
PORT = 2000
BUFFER_SIZE = 1024


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(str.encode(argv[1]), (HOST, PORT))
    data, server = sock.recvfrom(BUFFER_SIZE)

    print(data.decode())