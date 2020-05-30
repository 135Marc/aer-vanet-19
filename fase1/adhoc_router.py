from adhoc_table import Table
from adhoc_hello import hello

class Router:
    zone = ''
    name = ''
    routingTable = None
    pendingTable = {}
    forwardingTable = {}

    def __init__(self, zone, name, routing_table):
        self.zone = zone
        self.name = name
        self.routingTable = routing_table

    def route(self, pdu):
        newpdu = None

        # Obter tipo do pdu, ttl e target
        pdu_type = pdu.getType()
        ttl = pdu.getTTL()
        target = pdu.getTarget()

        # Verificar tempo de vida do pdu caso seja positivo verifica o tipo de pdu.
        if ttl <= 0:
            print('[TTL expired]', pdu_type)
        elif pdu_type == 'HELLO':
            hello(self.zone, self.name, pdu, self.routingTable)
        elif pdu_type.split('_')[0] == 'ROUTE':
            print(pdu_type)
            if not self.routingTable.exists(target):
                newpdu = pdu
        else:
            print('[PDU TYPE unknown]', pdu_type)

        # Verificar se o nó já existe na tabela
        # row = self.routingTable.exists()
        # if row:
        #     print('Face | Neighbour | Content )
        #     print(row[0] , row[1], row[2])
        # elif pdu.getType() == 'ROUTE_REQUEST' or pdu.getType() == 'METHOD_REQUEST':
        #         rplyawait.addElem(pdu.getTarget())

        #         #Criar tread para remover elemento do array ao fim de um periodo de tempo
        #         t = threading.Thread(target=rmAwaitPdu, args=(rplyawait,pdu.getTarget(), interval, answersr,answersm, pdu.getType()))
        #         t.start()
            
        return newpdu