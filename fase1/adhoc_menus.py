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
            # Verificar se existe, ou não, um pdu para enviar. 
            if not router.routingTable.exists(cmd[1]):
                pdu = PDU('ROUTE_REQUEST', name, None, radius, None, cmd[1], [name])
                pdu = router.route(pdu)
                dispatch_queue.put(pdu)
            else:
                print('----------------------------')
                print('Face | Neighbour | Content ')
                row = router.routingTable.exists(cmd[1])
                print(row[0], '  ', row[1], '  ', row[2])
                print('----------------------------')
        
        # Operação padrão
        else:
            print('Opção inválida.')