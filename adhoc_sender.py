import pickle
import time
from adhoc_pdu import PDU

def sender(socket, name, port, groupipv6, routing_table, interval):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    while True:
        pdu = PDU(name, "HELLO" + name, 1, routing_table)
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        time.sleep(interval)