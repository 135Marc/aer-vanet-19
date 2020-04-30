import pickle
import time
import struct
import queue
from adhoc_pdu import PDU
from adhoc_table import Table

def receiver(socket, name, port, groupipv6, routing_table, interval, msgqueue):
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
        if pdu.getType() == 'HELLO':
            #print('Tipo: ' + pdu.getType() + ' Origem: ' + pdu.getSource())
            nodetime = time.time()
            routing_table.addNode(pdu.getSource(), pdu.getSource(), str(sender[0]).split('%')[0], nodetime)
            routing_table.addNeighbour(pdu.getSource(), pdu.getSource(), str(sender[0]).split('%')[0], nodetime)
            routing_table.mergeTable(pdu.getTable(), pdu.getSource(), nodetime, name)
            routing_table.verifyTimes(interval)
            #routing_table.printTable()
        elif pdu.getType() == 'ROUTE_REPLY':
            pdu.printPDU()
        elif pdu.getType() == 'ROUTE_REQUEST':
            nodo = routing_table.exists(pdu.getTarget())
            msg = nodo[0] + ' ' + nodo[2]
            if nodo:
                newpdu = PDU(name, 'ROUTE_REPLY', 5, Table(), pdu.getSource(), msg,[])
                msgqueue.put(newpdu)
            elif pdu.getTarget() == name:
                print('O nodo procurado é de nivel 1!')
            else:
                print('Reencaminhar!')