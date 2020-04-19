#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.

#Nome do nodo:
#> python3 adhoc_app.py NOME

MYPORT = 9999
MYGROUP_6 = 'ff02::1'
NAME = ''
ROUTING = ''

from adhoc_pdu import PDU
from adhoc_table import Table
import time
import struct
import socket
import sys
import threading
import pickle
import random

def main():
    if len(sys.argv) > 1:
        NAME = sys.argv[1]
    else:
        NAME = str(random.uniform(0, 100))
    print('Nodo: ' + NAME)
    ROUTING = Table()
    ROUTING.addNode(NAME, NAME, '::1')
    ROUTING.printTable()
    x = threading.Thread(target=sender, args=())
    x.start()
    y = threading.Thread(target=receiver, args=())
    y.start()

def sender():
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    while True:
        pdu = PDU(NAME, "HELLO", 1)
        sock.sendto(pickle.dumps(pdu), (MYGROUP_6, MYPORT))
        time.sleep(5)


def receiver():
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(MYGROUP_6, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Bind it to the port
    s.bind(('', MYPORT))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
    mreq = group_bin + struct.pack('@I', 0)
    s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    # Loop, printing any data we receive
    while True:
        data, sender = s.recvfrom(1500)
        #while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
        pdu = pickle.loads(data)
        ROUTING.addNode(pdu.getNode(), pdu.getNode(), str(sender[0]))
        print ('Tipo: ' + pdu.getType())
        print ('TTL: ' + str(pdu.getTTL()))
        ROUTING.printTable()


if __name__ == '__main__':
    main()
