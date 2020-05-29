import pickle
import time
import threading
import queue
from adhoc_pdu import PDU
from adhoc_table import Table
from adhoc_pdutimer import rmAwaitPdu

def sender(socket, name, port, groupipv6, routing_table, interval, msgqueue, rplyawait, answersr, answersm):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    # (ROUTE_REPLY|ROUTE_REQUEST) Enviar pdus em fila de espera 
    rr = threading.Thread(target=dispatch, args=(sock,msgqueue,groupipv6,port,rplyawait,interval,name, answersr, answersm))
    rr.start()

    # (Protocolo HELLO) Atualizar tabelas de roteamento 
    while True:
        pdu = PDU(name, 'HELLO', 1, routing_table)
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        time.sleep(interval)

def dispatch(sock, msgqueue, groupipv6, port, rplyawait, interval, name, answersr, answersm):
    while True:
        # Obter proxima mensagem
        pdu = msgqueue.get()
        # Adicionar elemento há lista de espera por respostas 
        if(pdu.getType() == 'ROUTE_REQUEST' or pdu.getType() == 'METHOD_REQUEST'):
            rplyawait.addElem(pdu.getTarget())
            #Criar tread para remover elemento do array ao fim de um periodo de tempo
            t = threading.Thread(target=rmAwaitPdu, args=(rplyawait,pdu.getTarget(), interval, answersr,answersm))
            t.start()
            
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))

    