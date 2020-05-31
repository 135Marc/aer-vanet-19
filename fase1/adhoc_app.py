#!/usr/bin/env python
import sys
import threading
import socket
import queue
from adhoc_listenner import listenner
from adhoc_sender import sender
from adhoc_menus import menus
from adhoc_table import Table
from adhoc_router import Router
from adhoc_pdu import PDU

# Network params
PORT = 9999
GROUPIPv6 = 'ff02::1'

# Host params
NAME = 'df_name'
ROUTING_TABLE = Table()
DISPATCH_QUEUE = queue.Queue(15)
FORWARD_QUEUE = queue.Queue(15)
HELLO_INTERVAL = 10
DEAD_INTERVAL = 10
TIMEOUT = 2
RADIUS = 10
ZONE = 'df_zone'
LOCK = threading.Lock()

def main():
    updateHostParams()
    ROUTER = Router(ZONE, NAME, ROUTING_TABLE, RADIUS, TIMEOUT,)
    
    # Menus
    # m = threading.Thread(target=menus, args=(NAME, ROUTER, RADIUS, DISPATCH_QUEUE))
    # m.start()

    # Obter e tratar datagramas UDP
    lt = threading.Thread(target=listenner, args=(socket, PORT, GROUPIPv6, ZONE, NAME, ROUTER, FORWARD_QUEUE,))
    lt.start()

    # Enviar datagramas UDP
    st = threading.Thread(target=sender, args=(socket, PORT, GROUPIPv6, NAME, ROUTING_TABLE, ZONE, HELLO_INTERVAL, DISPATCH_QUEUE, FORWARD_QUEUE,))
    st.start()

    # Host a escuta
    print('[HOST]', NAME + ':' + str(PORT))
    print('---------Opções:-----------')
    print('Encontrar nodo: find')
    print('Imprimir tabela: print')
    print('---------------------------')

    while True:
        opt = input()
        cmd = opt.split(' ')

        # Imprimir tabela
        if cmd[0] == 'print':
            ROUTER.routingTable.printTable()
        
        # Encontrar novo nodo
        elif cmd[0] == 'find':
            print('0-------')
            # Verificar se existe, ou não, um pdu para enviar. 
            print('1-------')
            if not ROUTER.routingTable.exists(cmd[1]):
                pdu = PDU('ROUTE_REQUEST', NAME, None, RADIUS, None, cmd[1], [NAME])
                
                print('2-------')
                DISPATCH_QUEUE.put(pdu)
                print('3-------')
            else:
                print('----------------------------')
                print('Face | Neighbour | Content ')
                row = ROUTER.routingTable.exists(cmd[1])
                print(row[0], '  ', row[1], '  ', row[2])
                print('----------------------------')
        
        # Operação padrão
        else:
            print('Opção inválida.')

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
tt = threading.Thread(target=ROUTING_TABLE.tableTimes, args=(DEAD_INTERVAL,))
tt.start()

if __name__ == '__main__':
    main()
