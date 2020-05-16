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
        # Obter o pdu recebido
        data, sender = s.recvfrom(4096)
        pdu = pickle.loads(data)

        # Remover nodos, da rede, da tabla pelo tempo de expiração.
        routing_table.verifyTimes(interval)
        
        # Obter informações do pdu
        pdutype = pdu.getType()
        path = pdu.getPath()
        source = pdu.getSource()
        ttl = pdu.getTTL()
        
        if ttl >= 0:
            # Verificar o tipo de pdu
            # Processar pedido HELLO recebido.
            if pdutype == 'HELLO':
                # Adicionar o nodo nas tabelas (geral e vizinhos diretos).
                # Juntar a tabela dos vizinhos do emissor do pdu recebido
                # com a tabela geral.
                nodetime = time.time()
                routing_table.addNode(source, source, str(sender[0]).split('%')[0], nodetime)
                routing_table.addNeighbour(source, source, str(sender[0]).split('%')[0], nodetime)
                routing_table.mergeTable(pdu.getTable(), source, nodetime, name)

            # Processar pedido ROUTE_REQUEST recebido.
            elif pdutype == 'ROUTE_REQUEST':

                # Verificar se a origem do datagrama não é este nodo;
                # Verificar se o pdu ainda não tinha passado por este nodo.
                if source != name and (name not in path):

                    # Verificar a tabela tem a informação do nodo procurado.
                    target = routing_table.exists(pdu.getTarget())
                    if target:
                        # ROUTE_REPLY caso o nodo procurado exista na tabela
                        msg = target[0] + ' ' + target[2]
                        pdu.replyPDU(name, source, msg)
                        msgqueue.put(pdu)
                        print('ROUTE_REQUEST Encontrado: ', source, ' -> ', name)

                    else:
                        # ROUTE_REQUEST caso o nodo procurado não exista na tabela
                        pdu.forwardingPDU(name)
                        msgqueue.put(pdu)
                        print('ROUTE_REQUEST Não Encontrado: ', source, ' -> *',  )
                else:
                    print('ROUTE_REQUEST Replicado: ', source)

            # Processar pedido ROUTE_REPLY recebido.
            elif pdutype == 'ROUTE_REPLY':
                if not routing_table.exists(pdu.getMsg().split(' ')[0]):
                    nodetime = time.time()
                    source = pdu.getSource()
                    target = pdu.getTarget()
                    msg = pdu.getMsg()
                    path = pdu.getPath()
                    poped = path[-1:]
                    if len(poped) == 1:
                        if poped[0] == name:
                            if rplyawait.checkElem(msg.split(' ')[0]):
                                rplyawait.rmElem(msg.split(' ')[0])
                                routing_table.addNode(msg.split(' ')[0], source, msg.split(' ')[1], nodetime)
                                pdu.forwardingPDU(name)
                                msgqueue.put(pdu)
                                print('Reencaminhar REPLY!')

                    elif target == name:
                        if rplyawait.checkElem(msg.split(' ')[0]):
                            rplyawait.rmElem(msg.split(' ')[0])
                            routing_table.addNode(msg.split(' ')[0], source, msg.split(' ')[1], nodetime)
                            print('Atualizar Tabela')
