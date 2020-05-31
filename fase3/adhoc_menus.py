from adhoc_pdu import PDU
from adhoc_pending_timer import pendingTimeout
import threading

def menus(name, router, radius, timeout, dispatch_queue):
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
                if router.pendingTable.check((cmd[1], 'ROUTE_REPLY')):
                    router.pendingTable.add((cmd[1],'ROUTE_REPLY'), name)
                    print('[ROUTE_REQUEST] already requested')
                else:
                    router.pendingTable.add((cmd[1],'ROUTE_REPLY'), name)
                    pdu = PDU('ROUTE_REQUEST', name, None, radius, None, cmd[1], [name])
                    dispatch_queue.put(pdu)

                    # Criar thread para remover elemento da pendingTable depois do passar o tempo de timeout
                    threading.Thread(target=pendingTimeout, args=(timeout, router.pendingTable, (cmd[1],'ROUTE_REPLY'),)).start()

            else:
                print('----------------------------')
                print('Face | Neighbour | Content ')
                row = router.routingTable.exists(cmd[1])
                print(row[0], '  ', row[1], '  ', row[2])
                print('----------------------------')
        
        elif cmd[0].upper() == 'pub':
            router.contentStore.addContent(cmd[1], cmd[2])
            print('[CONTENT] added')
        elif cmd[0].upper() == 'sub':
            # Verificar se existe, ou não, um pdu para enviar. 
            if not router.contentStore.checkContent(cmd[1]):
                if router.pendingInterestTable.check(cmd[1]):
                    router.pendingInterestTable.add(cmd[1], name)
                    print('[CONTENT] already requested')
                else:
                    router.pendingInterestTable.add(cmd[1], name)
                    pdu = PDU('CONTENT_REQUEST', name, None, radius, None, cmd[1], [name])
                    dispatch_queue.put(pdu)

                    # Criar thread para remover elemento da pendingTable depois do passar o tempo de timeout
                    threading.Thread(target=pendingTimeout, args=(timeout, router.pendingInterestTable, (cmd[1],'CONTENT_REPLY'),)).start()

            else:
                print('----------------------------')
                print('Face | Neighbour | Content ')
                row = router.routingTable.exists(cmd[1])
                print(row[0], '  ', row[1], '  ', row[2])
                print('----------------------------')
        # Operação padrão
        else:
            print('Opção inválida.')