import pickle
import time
import threading
import queue
from adhoc_pdu import PDU
from adhoc_table import Table

def sender(socket, name, port, groupipv6, routing_table, interval, msgqueue):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    rr = threading.Thread(target=route_request, args=(sock,msgqueue,groupipv6,port,))
    rr.start()

    while True:
        pdu = PDU(name, 'HELLO', 1, routing_table)
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        time.sleep(interval)

def route_request(sock, msgqueue, groupipv6, port):
    while True:
        print('Wainting!')
        pdu = msgqueue.get()
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))