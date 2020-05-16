import queue
from adhoc_pdu import PDU

def menus(source, msgqueue, table):
    print('Nodo: ' + source)
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
            newpdu = PDU(source, 'ROUTE_REQUEST', 5, None, nodo, '', [source])
            msgqueue.put(newpdu)
        else:
            print('Opção inválida.')

