from adhoc_pdu import PDU

def menus(lock, name, router, radius, dispatch_queue):
    print('---------Opções:-----------')
    print('Encontrar nodo: find')
    print('Imprimir tabela: print')
    print('---------------------------')

    while True:
        opt = input()
        cmd = opt.split(' ')

        # Imprimir tabela
        if cmd[0] == 'print':
            lock.acquire()
            router.routingTable.printTable()
            lock.release()
        
        # Encontrar novo nodo
        elif cmd[0] == 'find':
            # Verificar se existe, ou não, um pdu para enviar. 
            lock.acquire()
            if not router.routingTable.exists(cmd[1]):
                pdu = PDU('ROUTE_REQUEST', name, None, radius, None, cmd[1], [name])
                dispatch_queue.put(pdu)
            else:
                print('----------------------------')
                print('Face | Neighbour | Content ')
                row = router.routingTable.exists(cmd[1])
                print(row[0], '  ', row[1], '  ', row[2])
                print('----------------------------')
            lock.release()
        
        # Operação padrão
        else:
            print('Opção inválida.')