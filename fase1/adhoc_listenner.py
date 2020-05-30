import socket
import pickle
import struct
from adhoc_pdu import PDU
from adhoc_router import Router

def listenner(socket, port, groupipv6, zone, name, router, dispatch_queue):
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(groupipv6, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Bind it to the port
    s.bind(('', port))
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])

    # Join group
    mreq = group_bin + struct.pack('@I', 0)
    s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    # Loop, get all pdu's
    while True:
        # Obter o pdu recebido
        data, sender = s.recvfrom(4096)
        pdu = pickle.loads(data)
        pdu.printPDU()
        pdu = router.route(pdu)

        if pdu:
            dispatch_queue.put(pdu)
        else:
            continue

