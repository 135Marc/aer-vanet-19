import queue
from adhoc_pdu import PDU

def menus(name, table):
    print('Nó: ' + name)
    print('---------Opções:-----------')
    print('Encontrar nodo: find')
    print('Imprimir tabela: print')
    print('---------------------------')

    while True:
        opt = input()
        cmd = opt.split(' ')

        # Imprimir tabela
        if opt[0] == 'print':
            table.printTable()
        
        # Encontrar novo nodo
        # elif opt[0] == 'find':
            # print('Nome do nodo:')
            # nodo = input()
            # newpdu = PDU(name, 'ROUTE_REQUEST', 5, None, nodo, '', [source])
            # msgqueue.put(newpdu)
        
        # Operação padrão
        else:
            print('Opção inválida.')