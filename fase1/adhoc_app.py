#!/usr/bin/env python
import sys
import threading
import socket
from adhoc_listenner import listenner
from adhoc_sender import sender
from adhoc_table import Table

# Network params
PORT = 9999
GROUPIPv6 = 'ff02::1'

# Host params
NAME = ''
ROUTING_TABLE = Table()
HELLO_INTERVAL = 10
DEAD_INTERVAL = 10
ZONE = 'df_zone'

def main():
    updateHostParams()
    # Obter e tratar datagramas UDP
    lt = threading.Thread(target=listenner, args=(socket, PORT, GROUPIPv6, NAME, ROUTING_TABLE, DEAD_INTERVAL,))
    lt.start()
    # Enviar datagramas UDP
    st = threading.Thread(target=sender, args=(socket, PORT, GROUPIPv6, NAME, ROUTING_TABLE, ZONE, HELLO_INTERVAL,))
    st.start()

def updateHostParams():
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            # Nome do nodo
            if(sys.argv[i] == '-n'):
                NAME = sys.argv[i+1]
            # Defenir dead interval
            if(sys.argv[i] == '-di'):
                DEAD_INTERVAL = int(sys.argv[i+1])
            # Defenir hello interval
            if(sys.argv[i] == '-hi'):
                HELLO_INTERVAL = int(sys.argv[i+1])
    else:
        print('Configurações do nodo:')
        print('-n: nome')
        print('-hi: hello interval')
        print('-di: dead interval')


if __name__ == '__main__':
    main()