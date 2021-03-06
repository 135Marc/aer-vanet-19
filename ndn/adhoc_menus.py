import queue
from adhoc_pdu import PDU

def menus(source, msgqueue, answers, cs, pit):
    print('Nodo: ' + source)
    print('---------Pedidos-----------')
    print('Publicar: pub data_name data_value')
    print('Subscrever: sub data_name')
    print('---------------------------')

    while True:
        opt = input()
        directive = opt.split(' ')

        # Publicar informação
        if directive[0].upper() == 'PUB':
            cs.addContent(directive[1], directive[2])
            print(opt)
        # Subscrever informação
        elif directive[0].upper() == 'SUB':
            content = directive[1]
            if cs.checkContent(content):
                print('Conteudo: ', cs.getContent(content))
            elif not pit.checkInterest(content):
                pit.addInterest(content, source)
                newpdu = PDU(source, 'SUB_REQUEST', 10, None, None, content)
                msgqueue.put(newpdu)
            else:
                print('Conteudo já procurado')
            ans = answers.get()
            print(ans)
        # Operação padrão
        else:
            print('Opção inválida.')