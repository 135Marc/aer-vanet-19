import threading
from adhoc_table import Table
from adhoc_hello import hello
from adhoc_pending_timer import pendingTimeout
from adhoc_pending import Pending
from adhoc_pdu import PDU

class Router:
    zone = ''
    name = ''
    radius = 0
    timeout = 0
    routingTable = None
    pendingTable = Pending()
    forwardingTable = {}

    def __init__(self, zone, name, routing_table, radius, timeout):
        self.zone = zone
        self.name = name
        self.routingTable = routing_table
        self.radius = radius
        self.timeout = timeout


    def route(self, pdu):
        newpdu = None

        # Obter tipo do pdu, ttl e target
        pdu_type = pdu.getType()
        ttl = pdu.getTTL()
        source = pdu.getSource()
        directive = pdu.getDirective()
        target = pdu.getTarget()

        # Verificar tempo de vida do pdu caso seja positivo verifica o tipo de pdu.
        if ttl <= 0 :
            print('[TTL expired]', pdu_type)
        elif source == self.name :
            newpdu = None
        elif pdu_type == 'HELLO':
            hello(self.zone, self.name, pdu, self.routingTable)
        elif pdu_type == 'ROUTE_REQUEST':
            found = self.routingTable.exists(directive)
            if found:
                strrow = found[0] + ' ' + found[1] + ' ' + found[2],
                newpdu = PDU('ROUTE_REPLY', self.name, source, self.radius, None, strrow, [self.name])
                print('[ROUTE_REQUEST] found')
            elif self.pendingTable.check((directive, 'ROUTE_REPLY')):
                self.pendingTable.add((directive,'ROUTE_REPLAY'), source)
                print('[ROUTE_REQUEST] already requested')
            else:
                self.pendingTable.add((directive,'ROUTE_REPLY'), source)
                newpdu = PDU('ROUTE_REQUEST', source, None, ttl-1, None, directive, [self.name])

                #Criar tread para remover elemento do array ao fim de um periodo de tempo
                pt = threading.Thread(target=pendingTimeout, args=(self.timeout, self.pendingTable, (directive,'ROUTE_REPLY'),))
                pt.start()

                print('[ROUTE_REQUEST] forward')

        elif pdu_type == 'ROUTE_REPLY':
            print('route_reply')
            # if self.pendingTable.check((source, 'ROUTE_REPLAY')):
            #    faces = self.pendingTable.get((source, 'ROUTE_REPLAY'))
            #    self.pendingTable.rm((source, 'ROUTE_REPLAY'))
            #    if self.name in faces:
            
            #   update own routingTable
            #   generate PDUs for pending face
            # else:
            #   continue 
        else:
            print('[PDU TYPE unknown]', pdu_type)

