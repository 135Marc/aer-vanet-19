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
from adhoc_pdu import PDU
from adhoc_table import Table
from adhoc_sender import sender
from adhoc_receiver import receiver

MYPORT = 9999
MYGROUP_6 = 'ff02::1'
NAME = ''
ROUTING = Table()

def main():
    INTERVAL = 10
    s = len(sys.argv)
    if s > 1:
        for i in range(1, s):
            if(sys.argv[i] == '-n'):
                NAME = sys.argv[i+1]
            if(sys.argv[i] == '-i'):
                INTERVAL = int(sys.argv[i+1])
    else:
        print('Configurações do nodo:')
        print('-n: nome')
        print('-i: intervalo')


    print('Nodo: ' + NAME)
    y = threading.Thread(target=receiver, args=(socket, NAME, MYPORT, MYGROUP_6, ROUTING,))
    y.start()
    x = threading.Thread(target=sender, args=(socket, NAME, MYPORT, MYGROUP_6, ROUTING, INTERVAL,))
    x.start()

if __name__ == '__main__':
    main()
