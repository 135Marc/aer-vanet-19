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
            pdu = router.route(pdu)
            # Verificar se existe, ou não, um pdu para enviar. 
            if pdu:
                dispatch_queue.put(pdu)
            else:
                print('Face | Neighbour | Content ')
                row = router.routingTable.exists(cmd[1])
                print(row[0] , row[1], row[2])
        
        # Operação padrão
        else:
            print('Opção inválida.')