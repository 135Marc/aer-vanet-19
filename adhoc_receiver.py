import pickle
import time
import struct

def receiver(socket, name, port, groupipv6, routing_table, interval):
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(groupipv6, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Bind it to the port
    s.bind(('', port))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
    mreq = group_bin + struct.pack('@I', 0)
    s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    # Loop, printing any data we receive
    while True:
        data, sender = s.recvfrom(4096)
        pdu = pickle.loads(data)
        nodetime = time.time()

        #print('Tipo: ' + pdu.getType() + ' Origem: ' + pdu.getSource())
        routing_table.addNode(pdu.getSource(), pdu.getSource(), str(sender[0]).split('%')[0], nodetime)
        routing_table.addNeighbour(pdu.getSource(), pdu.getSource(), str(sender[0]).split('%')[0], nodetime)
        routing_table.mergeTable(pdu.getTable(), pdu.getSource(), nodetime, name)
        routing_table.verifyTimes(interval)
        #routing_table.printTable()