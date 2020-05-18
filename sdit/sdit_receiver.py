import pickle
import time
import struct

def receiver(s, port, groupipv6):
    # Create a socket
    s.bind((groupipv6, port))
    s.listen()
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
