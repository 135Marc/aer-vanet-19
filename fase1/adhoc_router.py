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
    dispatchQueue = None

    def __init__(self, zone, name, routing_table, radius, timeout, dispatch_queue):
        self.zone = zone
        self.name = name
        self.routingTable = routing_table
        self.radius = radius
        self.timeout = timeout
        self.dispatchQueue = dispatch_queue


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
                strrow = str(found[0]) + ' ' + str(found[2])
                newpdu = PDU('ROUTE_REPLY', self.name, source, self.radius, None, strrow, [self.name])
                print('[ROUTE_REQUEST] found')
            elif self.pendingTable.check((directive, 'ROUTE_REPLY')):
                self.pendingTable.add((directive,'ROUTE_REPLY'), source)
                print('[ROUTE_REQUEST] already requested')
            else:
                self.pendingTable.add((directive,'ROUTE_REPLY'), source)
                newpdu = PDU('ROUTE_REQUEST', source, None, ttl-1, None, directive, [self.name])

                #Criar thread para remover elemento da pendingTable depois do passar o tempo de timeout
                pt = threading.Thread(target=pendingTimeout, args=(self.timeout, self.pendingTable, (directive,'ROUTE_REPLY'),))
                pt.start()

                print('[ROUTE_REQUEST] forward')

        elif pdu_type == 'ROUTE_REPLY':
            row = directive.split(' ')
            if self.pendingTable.check((row[0], 'ROUTE_REPLY')):
                faces = self.pendingTable.get((row[0], 'ROUTE_REPLY'))
                print(faces)
                self.pendingTable.rm((row[0], 'ROUTE_REPLY'))
                if self.name in faces:
                    self.routingTable.addNode(row[0], source, row[1], time.time())
                    faces.remove(self.name)
                    print('[ROUTE_REPLY] tabela de routing atualizada')
                
                for face in faces:
                    newpdu = PDU('ROUTE_REPLY', self.name, source, self.radius, None, directive, [self.name])
                    self.dispatchQueue.put(newpdu)
                print('[ROUTE_REPLY] forward')
                newpdu = None
        else:
            print('[PDU TYPE unknown]', pdu_type)
        return newpdu