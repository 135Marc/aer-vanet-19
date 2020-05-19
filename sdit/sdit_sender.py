import pickle
import socket

socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

def sender(port, groupipv6):
    socket.connect((groupipv6, port))

    while True:
        msg = input('-----msg------')
        socket.sendto(msg.encode('utf-8'), (groupipv6, port))

    