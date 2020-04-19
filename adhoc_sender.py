import pickle
import socket
import time
from adhoc_pdu import PDU

def sender(name, port, groupipv6, routing_table):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)

    while True:
        time.sleep(5)
        pdu = PDU(name, "HELLO" + name, 1, routing_table)
        print('----------------Rows do pdu sender---------------------')
        for node in pdu.getTable().getRows():
            print(node[0] + ' | ' + node[1] + ' | ' + node[2])
        sock.sendto(pickle.dumps(pdu), (groupipv6, port))
        time.sleep(20)