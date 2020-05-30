import pickle
import time
import threading
from adhoc_pdu import PDU
from adhoc_table import Table

def sender(socket, port, groupipv6, name, routing_table, zone, hello_interval, dispatch_queue):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    # Enviar pdu's HELLO a cada hello_interval
    ht = threading.Thread(target=hello, args=(sock, groupipv6, port, zone, name, routing_table, hello_interval,))
    ht.start()

    while True:
        # Obter proximo pdu
        pdu = dispatch_queue.get()

        # # Obter dados do pdu
        # pdu_type = pdu.getType()
        # target = pdu.getTarget()

        # # Verificar se o nó já existe na tabela
        # row = routing_table.exists()
        # if row:
        #     print('Face | Neighbour | Content )
        #     print(row[0] , row[1], row[2])
        # else: 
            
        #     if(pdu.getType() == 'ROUTE_REQUEST' or pdu.getType() == 'METHOD_REQUEST'):
        #         rplyawait.addElem(pdu.getTarget())
        #         #Criar tread para remover elemento do array ao fim de um periodo de tempo
        #         t = threading.Thread(target=rmAwaitPdu, args=(rplyawait,pdu.getTarget(), interval, answersr,answersm, pdu.getType()))
        #         t.start()
            
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))

def hello(sock, groupipv6, port, zone, name, routing_table, hello_interval):
    while True:
        pdu = PDU('HELLO', name, None, 1, routing_table, zone, [name])
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        time.sleep(hello_interval)
