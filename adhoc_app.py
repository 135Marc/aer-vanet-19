#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.

#Nome do nodo:
#> python3 adhoc_app.py NOME

MYPORT = 9999
MYGROUP_6 = 'ff02::1'
NAME = ''

table = {
}

import time
import struct
import socket
import sys
import threading
import json
import random

def main():
    if len(sys.argv) > 1:
        NAME = sys.argv[1]
    else
        NAME = str(random.uniform(0, 100))
    print('Nodo: ' + NAME)
    x = threading.Thread(target=sender, args=(NAME))
    x.start()
    y = threading.Thread(target=receiver, args=(NAME))
    y.start()

def sender(name):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    while True:
        pdu = """
        {
            "nome": "nome do nodo",
            "type": "HELLO",
            "ttl": 1
        }
        """
        sock.sendto(pdu.encode('utf-8'), (MYGROUP_6, MYPORT))
        time.sleep(5)


def receiver(name):
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
        while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
        pdu = json.loads(data.decode('utf-8'))
        table["peer_" + str(sender[1])] = str(sender[0])
        print (str(sender))
        print (pdu["type"])
        print ("------------")
        print (table)
        print ("------------")


if __name__ == '__main__':
    main()
