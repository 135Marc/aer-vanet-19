import queue
from adhoc_pdu import PDU

def menus(source, msgqueue, table):
    while True:
        print('---------Opções:-----------')
        print('Encontrar nodo: f')
        print('Imprimir tabela: p')
        print('---------------------------')
        opt = input()
        if opt == 'p':
            table.printTable()
        elif opt == 'f':
            print('Nome do nodo:')
            nodo = input()
            print('TTL:')
            ttl = int(input())
            newpdu = PDU(source, 'ROUTE_REQUEST', ttl, None, nodo, '')
            msgqueue.put(newpdu)
        else:
            print('Opção inválida.')

