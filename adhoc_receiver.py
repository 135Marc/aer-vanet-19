import pickle
import time
import struct
import queue
from adhoc_pdu import PDU
from adhoc_table import Table

def receiver(socket, name, port, groupipv6, routing_table, interval, msgqueue, rplyawait):
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
        routing_table.verifyTimes(interval)
        
        pdutype = pdu.getType()
        if pdutype == 'HELLO':
            nodetime = time.time()
            routing_table.addNode(pdu.getSource(), pdu.getSource(), str(sender[0]).split('%')[0], nodetime)
            routing_table.addNeighbour(pdu.getSource(), pdu.getSource(), str(sender[0]).split('%')[0], nodetime)
            routing_table.mergeTable(pdu.getTable(), pdu.getSource(), nodetime, name)
        elif pdutype == 'ROUTE_REPLY':
            if not routing_table.exists(pdu.getMsg().split(' ')[0]):
                nodetime = time.time()
                source = pdu.getSource()
                target = pdu.getTarget()
                ttl = pdu.getTTL()
                msg = pdu.getMsg()
                path = pdu.getPath()
                poped = path[-1:]
                if len(poped) == 1:
                    if poped[0] == name:
                        routing_table.addNode(msg.split(' ')[0], source, msg.split(' ')[1], nodetime)
                        pdu.forwardingPDU(name)
                        msgqueue.put(pdu)
                        print('Reencaminhar REPLY!')

                elif target == name:
                    if  checkElem(msg.split(' ')[0])
                        routing_table.addNode(msg.split(' ')[0], source, msg.split(' ')[1], nodetime)
                        print('Atualizar Tabela')
            
        elif pdutype == 'ROUTE_REQUEST':
            source = pdu.getSource()
            target = routing_table.exists(pdu.getTarget())
            ttl = pdu.getTTL()
            path = pdu.getPath()

            if source != name and name not in path:
                if target:
                    #ROUTE_REPLY caso o nodo procurado exista na tabela
                    msg = target[0] + ' ' + target[2]
                    pdu.replyPDU(name, source, msg)
                    msgqueue.put(pdu)
                    print('Responder!')
                elif ttl > 0:
                    #ROUTE_REQUEST caso o nodo procurado não exista na tabela
                    pdu.forwardingPDU(name)
                    msgqueue.put(pdu)
                    print('Reencaminhar REQUEST!')
                else:
                    print('O ttl do pdu expirou!')
