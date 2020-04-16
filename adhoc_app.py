#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.

MYPORT = 9999
MYGROUP_6 = 'ff02::1'
MYTTL = 1 # Increase to reach other networks

table = {}

import time
import struct
import socket
import sys
import threading

def main():
    x = threading.Thread(target=sender, args=())
    x.start()
    y = threading.Thread(target=receiver, args=())
    y.start()

def sender():
  sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
  sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

  ttl_bin = struct.pack('@I', MYTTL)
  sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

  while True:
    sock.sendto('HELLO'.encode('utf-8'), (MYGROUP_6, MYPORT))
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
        print (str(sender) + '  ' + data.decode('utf-8'))


if __name__ == '__main__':
    main()
