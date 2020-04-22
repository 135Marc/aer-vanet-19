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
INTERVAL = 10

def main():
    s = len(sys.argv)
    if s > 1:
        for i in range(1, s)
            switch(sys.argv[i])
                case '-n':
                        NAME = sys.argv[i+1]
                        break
                case '-i':
                        INTERVAL = int(sys.argv[i+1])
                        break
        NAME = sys.argv[1]
    else:
        print('-n: nome')
        print('-i: intervalo')
    print('Nodo: ' + NAME)
    ROUTING.addNode(NAME, NAME, MYGROUP_6)
    y = threading.Thread(target=receiver, args=(socket, NAME, MYPORT, MYGROUP_6, ROUTING, INTERVAL,))
    y.start()
    x = threading.Thread(target=sender, args=(socket, NAME, MYPORT, MYGROUP_6, ROUTING,))
    x.start()

if __name__ == '__main__':
    main()
