import queue
from adhoc_pdu import PDU

def menus(source, msgqueue, cs, pit):
    while True:
        print('Nodo: ' + source)
        print('---------Pedidos-----------')
        print('Publicar: pub data_name data_value')
        print('Subscrever: sub data_name')
        print('---------------------------')

        opt = input()
        opt.split(' ')

        # Publicar informação
        if opt[0].upper() == 'PUB':
            cs.addContent(opt[1], opt[2])
            print(opt)
        # Subscrever informação
        elif opt[0].upper() == 'SUB':
            content = pdu.getMsg()
            if cs.checkContent(content):
                print('Conteudo: ', cs.getContent(content))
            elif not pit.checkInterest(content):
                pit.addInterest(pdu.getMsg())
                newpdu = PDU(source, 'SUB_REQUEST', 10, None, None, opt[1], [source])
                msgqueue.put(newpdu)
            else:
                print('Conteudo já procurado')

        # Operação padrão
        else:
            print('Opção inválida.')