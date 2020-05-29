import pickle
import time
import threading
from adhoc_pdu import PDU
from adhoc_table import Table

def sender(socket, port, groupipv6, name, routing_table, zone, hello_interval):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    # Enviar pdu's HELLO a cada hello_interval
    ht = threading.Thread(target=hello, args=(port, groupipv6, zone, name, routing_table, hello_interval,))
    ht.start()

def hello(port, groupipv6, zone, source, routing_table, hello_interval):
    while True:
        pdu = PDU('HELLO', source, None , 1, routing_table, zone, [source])
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        time.sleep(hello_interval)
