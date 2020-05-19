import pickle
import time
import struct
import socket

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

def receiver(port, groupipv6):
    # Create a socket
    s.bind((groupipv6, port))
    s.listen(5)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        # Loop, printing any data we receive
        while True:
            # Obter o pdu recebido
            data, sender = s.recvfrom(4096)
            if not data:
                break

            print(pdu.decode('utf-8'))
