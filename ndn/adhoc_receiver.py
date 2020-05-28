import pickle
import time
import struct
import queue
import socket
from adhoc_pdu import PDU
from adhoc_table import Table
from adhoc_tcp_server_api import get


def receiver(socket, name, port, groupipv6, routing_table, interval, msgqueue, rplyawait, answers, cs, pit, fib):
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
            if pdutype == 'SUB_REQUEST':
                content = pdu.getMsg()
                if cs.checkContent(content):
                    value = cs.getContent(content)
                    newpdu = PDU(name, 'SUB_DATA', 100, None, source, content + ' ' + value)
                    msgqueue.put(newpdu)
                    print('[SUB_REQUEST] Informação encontrada:', content)
                elif pit.checkInterest(content):
                    pit.addInterest(content, source)
                elif fib.checkInterface(content):
                    pit.addInterest(content, source)
                    interface = fib.getInterface(content)[0]
                    newpdu = PDU(name, 'SUB_REQUEST', ttl-1, None, source, content)
                    msgqueue.put(newpdu)
                    print('[SUB_REQUEST] Informação reencaminhada:', content)
                else:
                    print('[SUB_REQUEST] Informação inexistente:', content)

            if pdutype == 'SUB_DATA':
                data = pdu.getMsg().split(' ')
                content = data[0]
                value = data[1]
                if pit.checkInterest(content):
                    interested = pit.getInterested(content)
                    pit.rmInterest(content)
                    cs.addContent(content, value)
                    for i in interested:
                        if i == name:
                            answers.put(content + ' ' + value)
                        else:
                            newpdu = PDU(name, 'SUB_DATA', 100, None, i, content + ' ' + value)
                            msgqueue.put(newpdu)
                        print('[SUB_REQUEST] Informação encontrada:', content)
                else:
                    print('[SUB_DATA] Descartado', content)







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

            # Processar pedido Method_REQUEST recebido.
            elif pdutype == 'METHOD_REQUEST':
                target = pdu.getTarget()
                if not routing_table.exists(target):
                    if target == name:
                        opt = pdu.getMsg()
                        print('receiver ' + pdu.getMsg())
                        rec_msg = get(opt, port)

                        # METHOD_REPLY caso o nodo procurado exista na tabela
                        pdutable = Table()
                        pdu.replyPDU(name, source, pdutable, 'METHOD_REPLY', rec_msg)
                        msgqueue.put(pdu)
                        print('[METHOD_REQUEST Encontrado] ', source, ' -> ', target[0])

                elif name not in path:
                    print('receiver ' + pdu.getMsg())
                    # METHOD_REQUEST caso o nodo procurado não exista na tabela
                    pdu.forwardingPDU(name)
                    msgqueue.put(pdu)
                    print('[METHOD_REQUEST Reencaminhar] ', source, ' -> *')

            # Processar pedido METHOD_REPLY recebido.
            elif pdutype == 'METHOD_REPLY':
                poped = path[-1:]
                
                # Verificar se é o próximo elemento do caminho e se estava a espera de resposta
                if len(poped) == 1:
                    if poped[0] == name:

                        # Verificar se este é o destino da informação
                        if pdu.getTarget() == name:
                            answers.put(pdu)
                            print('[METHOD_REPLY Atualizar Tabela] ', source, ' -> ', name)

                        else:
                            pdu.forwardingPDU(name)
                            msgqueue.put(pdu)
                            print('[METHOD_REPLY Reencaminhar] ', source, ' -> *')

            # Processar pedido ROUTE_REQUEST recebido.
            elif pdutype == 'ROUTE_REQUEST':

                # Verificar se a origem do datagrama não é este nodo;
                # Verificar se o pdu ainda não tinha passado por este nodo.
                if source != name and (name not in path):

                    # Verificar a tabela tem a informação do nodo procurado.
                    target = routing_table.exists(pdu.getTarget())
                    if target:
                        # ROUTE_REPLY caso o nodo procurado exista na tabela
                        pdutable = Table()
                        pdutable.addNeighbour(target[0], None, target[2], -1)
                        pdu.replyPDU(name, source, pdutable, 'ROUTE_REPLY')
                        msgqueue.put(pdu)
                        print('[ROUTE_REQUEST Encontrado] ', source, ' -> ', target[0])

                    else:
                        # ROUTE_REQUEST caso o nodo procurado não exista na tabela
                        pdu.forwardingPDU(name)
                        msgqueue.put(pdu)
                        print('[ROUTE_REQUEST Não Encontrado] ', source, ' -> *')

                else:
                    print('[ROUTE_REQUEST  Replicado] ', source, ' -> ', name)

            # Processar pedido ROUTE_REPLY recebido.
            elif pdutype == 'ROUTE_REPLY':    
                nodetime = time.time()
                waited = list(pdu.getTable().getNeighbours())[0]
                poped = path[-1:]
                
                # Verificar se é o próximo elemento do caminho e se estava a espera de resposta
                if len(poped) == 1 and waited:
                    if poped[0] == name and rplyawait.checkElem(waited[0]):
                        rplyawait.rmElem(waited[0])
                        routing_table.addNode(waited[0], source, waited[2], nodetime)

                        # Verificar se este é o destino da informação
                        if pdu.getTarget() == name:
                            ## tabela atualizada
                            answers.put('table updated')
                            print('[ROUTE_REPLY Atualizar Tabela] ', source, ' -> ', name)

                        else:
                            pdu.forwardingPDU(name)
                            msgqueue.put(pdu)
                            print('[ROUTE_REPLY Reencaminhar] ', source, ' -> *')
    