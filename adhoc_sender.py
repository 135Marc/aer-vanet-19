import pickle
import socket
from adhoc_pdu import PDU

MYPORT = 9999
MYGROUP_6 = 'ff02::1'

def sender(name):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    while True:
        pdu = PDU(name, "HELLO", 1)
        sock.sendto(pickle.dumps(pdu), (MYGROUP_6, MYPORT))
        time.sleep(5)