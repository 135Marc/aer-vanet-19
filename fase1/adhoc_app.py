#!/usr/bin/env python
import sys
import socket
from multiprocessing import Process, Queue
from multiprocessing import Process, Lock
from adhoc_listenner import listenner
from adhoc_sender import sender
from adhoc_menus import menus
from adhoc_table import Table
from adhoc_router import Router

# Network params
PORT = 9999
GROUPIPv6 = 'ff02::1'

# Host params
NAME = 'df_name'
ROUTING_TABLE = Table()
HELLO_INTERVAL = 10
DEAD_INTERVAL = 10
TIMEOUT = 1
RADIUS = 10
ZONE = 'df_zone'

def main():
    updateHostParams()
    DISPATCH_QUEUE = Queue()
    ROUTER = Router(ZONE, NAME, ROUTING_TABLE, RADIUS, TIMEOUT,)
    LOCK = Lock()
    
    # Menus
    Process(target=menus, args=(LOCK, NAME, ROUTER, RADIUS, DISPATCH_QUEUE)).start()

    # Obter e tratar datagramas UDP
    Process(target=listenner, args=(LOCK, socket, PORT, GROUPIPv6, ZONE, NAME, ROUTER, DISPATCH_QUEUE,)).start()

    # Enviar datagramas UDP
    Process(target=sender, args=(LOCK, socket, PORT, GROUPIPv6, NAME, ROUTING_TABLE, ZONE, HELLO_INTERVAL, DISPATCH_QUEUE)).start()

    # Host a escuta
    print('[HOST]', NAME + ':' + str(PORT))

def updateHostParams():
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            # Nome do nodo
            if(sys.argv[i] == '-n'):
                global NAME
                NAME = sys.argv[i+1]
            # Defenir dead interval
            if(sys.argv[i] == '-di'):
                global DEAD_INTERVAL
                DEAD_INTERVAL = int(sys.argv[i+1])
            # Defenir hello interval
            if(sys.argv[i] == '-hi'):
                global HELLO_INTERVAL
                HELLO_INTERVAL = int(sys.argv[i+1])
            # Zona onde o veiculo se encontra
            if(sys.argv[i] == '-r'):
                global RADIUS
                RADIUS = sys.argv[i+1]
            # Zona onde o veiculo se encontra
            if(sys.argv[i] == '-t'):
                global TIMEOUT
                TIMEOUT = sys.argv[i+1]
            # Zona onde o veiculo se encontra
            if(sys.argv[i] == '-z'):
                global ZONE
                ZONE = sys.argv[i+1]
    else:
        print('Configurações do nodo:')
        print('-n: nome')
        print('-hi: hello interval')
        print('-di: dead interval')


# Ativar operação de limpesa das tabelas por tempo
Process(target=ROUTING_TABLE.tableTimes, args=(DEAD_INTERVAL,)).start()

if __name__ == '__main__':
    main()
