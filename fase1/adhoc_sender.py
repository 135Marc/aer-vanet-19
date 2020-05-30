import pickle
import time
from multiprocessing import Process
from adhoc_pdu import PDU
from adhoc_table import Table

def sender(lock, socket, port, groupipv6, name, routing_table, zone, hello_interval, dispatch_queue):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    # Enviar pdu's HELLO a cada hello_interval
    ht = Pocess(target=hello, args=(sock, groupipv6, port, zone, name, routing_table, hello_interval,))
    ht.start()

    while True:
        lock.acquire()
        # Obter proximo pdu
        pdu = dispatch_queue.get()
        lock.release()
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))

def hello(sock, groupipv6, port, zone, name, routing_table, hello_interval):
    while True:
        pdu = PDU('HELLO', name, None, 1, routing_table, zone, [name])
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        time.sleep(hello_interval)
