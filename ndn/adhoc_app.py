import sys
import threading
import random
import socket
import queue
from adhoc_table import Table
from adhoc_replyawait import ReplyWait
from adhoc_sender import sender
from adhoc_receiver import receiver
from adhoc_menus import menus
from adhoc_tcp_client_api import get
from CS import ContentStore
from PIT import PendingInterestTable
from FIB import ForwardingInformationBase

MYPORT = 9919
MYGROUP_6 = 'ff02::1'
NAME = ''
ROUTING = Table()
MSGQUEUE = queue.Queue(15)
ANSWERS = queue.Queue(15)
RPLYAWAIT = ReplyWait()
PIT = PendingInterestTable()

def main():
    INTERVAL = 10
    CLIENT = False
    s = len(sys.argv)
    if s > 1:
        for i in range(1, s):
            # Nome do nodo
            if(sys.argv[i] == '-n'):
                NAME = sys.argv[i+1]
            # Defenir intervalo de "refresh"
            if(sys.argv[i] == '-i'):
                INTERVAL = int(sys.argv[i+1])
    else:
        print('Configurações do nodo:')
        print('-n: nome')
        print('-i: intervalo')
    
    # Menus
    m = threading.Thread(target=menus, args=(NAME, MSGQUEUE, CS, PIT,))
    m.start()
    # Obter datagramas UDP para o protocaolo HELLO e ROUTE_REQUEST
    r = threading.Thread(target=receiver, args=(socket, NAME, MYPORT, MYGROUP_6, ROUTING, INTERVAL, MSGQUEUE, RPLYAWAIT, ANSWERS, CS, PIT, FIB, ))
    r.start()
    # Despachar datagramas UDP para o protocolo HELLO e de datagramas de travessia
    s = threading.Thread(target=sender, args=(socket, NAME, MYPORT, MYGROUP_6, ROUTING, INTERVAL, MSGQUEUE, RPLYAWAIT, ANSWERS,))
    s.start()

if __name__ == '__main__':
    main()
