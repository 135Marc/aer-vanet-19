from adhoc_table import Table
from adhoc_hello import hello
from adhoc_Pending import Pending

class Router:
    zone = ''
    name = ''
    radius = 0
    routingTable = None
    pendingTable = Pending()
    forwardingTable = {}

    def __init__(self, zone, name, routing_table, radius):
        self.zone = zone
        self.name = name
        self.routingTable = routing_table
        self.radius = radius

    def route(self, pdu):
        newpdu = None

        # Obter tipo do pdu, ttl e target
        pdu_type = pdu.getType()
        ttl = pdu.getTTL()
        source = pdu.getSource()
        directive = pdu.getDirective()
        target = pdu.getTarget()

        # Verificar tempo de vida do pdu caso seja positivo verifica o tipo de pdu.
        if ttl <= 0:
            print('[TTL expired]', pdu_type)
        elif pdu_type == 'HELLO':
            hello(self.zone, self.name, pdu, self.routingTable)
        elif pdu_type == 'ROUTE_REQUEST':
            found = self.routingTable.exists(target)
            if found:
                newpdu = PDU('ROUTE_REPLAY', target, source, self.radius, None, found[2], [self.name])
            elif self.pendingTable.check((target, pdu_type)):
                self.pendingTable.add((target,pdu_type), source)
            else:
                newpdu = PDU('ROUTE_REQUEST', source, target, ttl-1, None, directive, [self.name]) 


        elif pdu_type == 'ROUTE_REPLY':
            # if replay on pendingTable:
            #   get pending faces of this target
            #   remove from pending
            #   update own routingTable
            #   generate PDUs for pending face
            # else:
            #   continue 
            continue
        else:
            print('[PDU TYPE unknown]', pdu_type)

        # Verificar se o nó já existe na tabela
        # elif pdu.getType() == 'ROUTE_REQUEST' or pdu.getType() == 'METHOD_REQUEST':
        #         rplyawait.addElem(pdu.getTarget())

        #         #Criar tread para remover elemento do array ao fim de um periodo de tempo
        #         t = threading.Thread(target=rmAwaitPdu, args=(rplyawait,pdu.getTarget(), interval, answersr,answersm, pdu.getType()))
        #         t.start()
            
        return newpdu