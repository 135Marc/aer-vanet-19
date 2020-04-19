#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.

#Nome do nodo:
#> python3 adhoc_app.py NOME

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
    if len(sys.argv) > 1:
        NAME = sys.argv[1]
    else:
        NAME = str(random.uniform(0, 100))
    print('Nodo: ' + NAME)
    ROUTING.addNode(NAME, NAME, str(socket.getaddrinfo(MYGROUP_6, None)[0][4][0]))
    x = threading.Thread(target=sender, args=(socket, NAME, MYPORT, MYGROUP_6, ROUTING,))
    x.start()
    y = threading.Thread(target=receiver, args=(socket, NAME, MYPORT, MYGROUP_6, ROUTING,))
    y.start()

if __name__ == '__main__':
    main()
