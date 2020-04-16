#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.

MYPORT = 9999
MYGROUP_6 = 'ff02::1'

table = {
}

import time
import struct
import socket
import sys
import threading
import json

def main():
    x = threading.Thread(target=sender, args=())
    x.start()
    y = threading.Thread(target=receiver, args=())
    y.start()

def sender():
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
        while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
        pdu = json.loads(data.decode('utf-8'))
        table["peer_" + str(sender[1])] = str(sender[0])
        print (pdu["type"])
        print ("------------")
        print (table)
        print ("------------")


if __name__ == '__main__':
    main()
