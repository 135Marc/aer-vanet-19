import pickle
import time
import threading
import queue
from adhoc_pdu import PDU
from adhoc_table import Table

def sender(socket, name, port, groupipv6, routing_table, interval, msgqueue):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    #Enviar pdus em fila de espera
    rr = threading.Thread(target=dispatch, args=(sock,msgqueue,groupipv6,port,))
    rr.start()

    #Atualizar tabelas de routeamento (Protocolo HELLO)
    while True:
        pdu = PDU(name, 'HELLO', 1, routing_table)
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        time.sleep(interval)

def dispatch(sock, msgqueue, groupipv6, port):
    while True:
        pdu = msgqueue.get()
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))