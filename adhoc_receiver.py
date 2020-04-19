import pickle
import struct
import socket


def receiver(name, port, groupipv6, routing_table):
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
        data, sender = s.recvfrom(4096)
        #while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
        pdu = pickle.loads(data)
        print ('Tipo: ' + pdu.getType())
        print ('TTL: ' + str(pdu.getTTL()))
        routing_table.addNode(pdu.getNode(), pdu.getNode(), str(sender[0]).split('%')[0])
        routing_table.printTable()