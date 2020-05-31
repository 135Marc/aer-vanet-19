import pickle
import time
import threading
from adhoc_pdu import PDU
from adhoc_table import Table

def sender(socket, port, groupipv6, name, routing_table, zone, hello_interval, dispatch_queue, forward_queue):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    # Enviar pdu's HELLO a cada hello_interval
    threading.Thread(target=hello, args=(sock, groupipv6, port, zone, name, routing_table, hello_interval,)).start()

    # Enviar pdu's reencaminhados
    threading.Thread(target=forward, args=(sock, groupipv6, port, forward_queue,)).start()

    while True:
        # Obter proximo pdu
        pdu = dispatch_queue.get()
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))

def forward(sock, groupipv6, port, forward_queue):
    while True:
        # Obter proximo pdu
        pdu = forward_queue.get()
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))

def hello(sock, groupipv6, port, zone, name, routing_table, hello_interval):
    while True:
        pdu = PDU('HELLO', name, None, 1, routing_table, zone, [name])
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        time.sleep(hello_interval)
