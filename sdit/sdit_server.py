import pickle
import time
import struct
import socket

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

def receiver(port, ipv6):
    # Create a socket
    s.bind((ipv6, port))
    print("s binded to port", port) 

    # put the s into listening mode 
    s.listen(5)

    while True:
        # establish connection with client 
        conn, addr = s.accept()
        print('Connected by', addr)
        
        # Obter o pdu recebido
        msg = conn.recv(1024)
        print(msg.decode('utf-8'))