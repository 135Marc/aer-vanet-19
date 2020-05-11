import pickle
import time
import threading
import queue
from adhoc_pdu import PDU
from adhoc_table import Table
from adhoc_pdutimer import rmAwaitPdu

def sender(socket, name, port, groupipv6, routing_table, interval, msgqueue, rplyawait):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    #Enviar pdus em fila de espera
    rr = threading.Thread(target=dispatch, args=(sock,msgqueue,groupipv6,port,rplyawait,interval,name,))
    rr.start()

    #Atualizar tabelas de roteamento (Protocolo HELLO)
    while True:
        pdu = PDU(name, 'HELLO', 1, routing_table)
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        time.sleep(interval)

def dispatch(sock, msgqueue, groupipv6, port, rplyawait, interval,name):
    while True:
        pdu = msgqueue.get()
        print('SENDER: ' + pdu.getSource() + ' != ' + name + ' and ' + name + ' not in [ ' + ','.join(pdu.getPath()) + ' ]')
        if(pdu.getType() == 'ROUTE_REQUEST'):
            print('Dispatch thread again')
            rplyawait.addElem(pdu.getTarget())
            #Criar tread para remover elemento do array ao fim de um periodo de tempo
            t = threading.Thread(target=rmAwaitPdu, args=(rplyawait,pdu.getTarget(), interval,))
            t.start()
            print('After thread')
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        print('After send')

    