import queue
from adhoc_pdu import PDU
from adhoc_table import Table

def menus(source, msgqueue, table):
    while True:
        print('---------Opções:-----------')
        print('Encontrar nodo: f')
        print('Imprimir tabela: p')
        print('---------------------------')
        opt = input()
        if(opt = 'p')
            table.printTable()
        elif(opt = 'f')
            print('Encontrar nodo:')
            nodo = input()
            newpdu = PDU(source, 'ROUTE_REQUES', 5, Table())
            msgqueue.put(newpdu)
        else
            print('Opção inválida.')

