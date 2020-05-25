#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.

#Nome do nodo:
#> python3 adhoc_app.py -n NOME 

#Intervalo entre pedidos HELLO, em segundos:
#> python3 adhoc_app.py -i INTERVALO

import sys
import threading
import random
import socket
import queue
from adhoc_table import Table
from adhoc_replyawait import ReplyWait
from adhoc_sender import sender
from adhoc_receiver import receiver
from adhoc_menus import menus, tcpserver

MYPORT = 9994
MYGROUP_6 = 'ff02::1'
NAME = ''
ROUTING = Table()
MSGQUEUE = queue.Queue(15)
RPLYAWAIT = ReplyWait()
SERVER = False

def main():
    INTERVAL = 10
    s = len(sys.argv)
    if s > 1:
        for i in range(1, s):
            # Nome do nodo
            if(sys.argv[i] == '-n'):
                NAME = sys.argv[i+1]
            # Defenir intervalo de "refresh"
            if(sys.argv[i] == '-i'):
                INTERVAL = int(sys.argv[i+1])
            # Ativar o modo servidor (por defeito é cliente)
            if(sys.argv[i] == '-s'):
                INTERVAL = True
    else:
        print('Configurações do nodo:')
        print('-n: nome')
        print('-i: intervalo')

    # Menus
    # m = threading.Thread(target=menus, args=(NAME, MSGQUEUE, ROUTING,))
    # m.start()
    # Ligação TCP para o sistema de difusão de informação de transito
    if SERVIDOR:
        t = threading.Thread(target=tcpserver, args=(NAME, MYPORT, ROUTING, MSGQUEUE,))
        t.start()
    # Obter datagramas UDP para o protocaolo HELLO e ROUTE_REQUEST
    r = threading.Thread(target=receiver, args=(socket, NAME, MYPORT, MYGROUP_6, ROUTING, INTERVAL, MSGQUEUE, RPLYAWAIT,))
    r.start()
    # Despachar datagramas UDP para o protocolo HELLO e de datagramas de travessia
    s = threading.Thread(target=sender, args=(socket, NAME, MYPORT, MYGROUP_6, ROUTING, INTERVAL, MSGQUEUE, RPLYAWAIT,))
    s.start()

if __name__ == '__main__':
    main()
