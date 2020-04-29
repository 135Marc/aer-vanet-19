import queue
from adhoc_pdu import PDU
from adhoc_table import Table

def menus(source, msgqueue):
    while True:
        print('---------Nodo a encontrar:-----------')
        nodo = input()
        print('-------------------------------------')
        newpdu = PDU(source, 'ROUTE_REQUES', 5, Table())
        msgqueue.put(newpdu)
