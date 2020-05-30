import queue
from adhoc_pdu import PDU

def menus(name, router, radius, dispatch_queue):
    print('---------Opções:-----------')
    print('Encontrar nodo: find')
    print('Imprimir tabela: print')
    print('---------------------------')

    while True:
        opt = input()
        cmd = opt.split(' ')

        # Imprimir tabela
        if cmd[0] == 'print':
            router.routingTable.printTable()
        
        # Encontrar novo nodo
        elif cmd[0] == 'find':
            pdu = PDU('ROUTE_REQUEST', name, cmd[1], radius, None, '', [source])
            dispatch_queue.put(pdu)
        
        # Operação padrão
        else:
            print('Opção inválida.')