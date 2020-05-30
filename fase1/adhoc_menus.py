import queue
from adhoc_pdu import PDU

def menus(name, table):
    print('---------Opções:-----------')
    print('Encontrar nodo: find')
    print('Imprimir tabela: print')
    print('---------------------------')

    while True:
        opt = input()
        cmd = opt.split(' ')

        # Imprimir tabela
        if opt[0] == 'prt':
            table.printTable()
        
        # Encontrar novo nodo
        # elif opt[0] == 'fnd':
            # print('Nome do nodo:')
            # nodo = input()
            # newpdu = PDU(name, 'ROUTE_REQUEST', 5, None, nodo, '', [source])
            # msgqueue.put(newpdu)
        
        # Operação padrão
        else:
            print('Opção inválida.')