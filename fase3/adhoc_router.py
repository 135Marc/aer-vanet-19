import threading
import time
from adhoc_table import Table
from adhoc_hello import hello
from adhoc_pending_timer import pendingTimeout
from adhoc_pending import Pending
from adhoc_pdu import PDU
from CS import ContentStore
from PIT import PendingInterestTable

class Router:
    zone = ''
    name = ''
    radius = 0
    timeout = 0
    contentStore = None
    pendingInterestTable = PendingInterestTable()
    routingTable = None
    pendingTable = Pending()
    forwardingTable = {}

    def __init__(self, zone, name, routing_table, radius, timeout):
        self.zone = zone
        self.name = name
        self.routingTable = routing_table
        self.contentStore = ContentStore(zone)
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
                strrow = str(found[0]) + ' ' + str(found[2])
                newpdu = PDU('ROUTE_REPLY', self.name, source, self.radius, None, strrow, [self.name])
                print('[ROUTE_REQUEST] found')
            elif self.pendingTable.check((directive, 'ROUTE_REPLY')):
                self.pendingTable.add((directive,'ROUTE_REPLY'), source)
                print('[ROUTE_REQUEST] already requested')
            else:
                self.pendingTable.add((directive,'ROUTE_REPLY'), source)
                newpdu = PDU('ROUTE_REQUEST', source, None, ttl-1, None, directive, [self.name])

                # Criar thread para remover elemento da pendingTable depois do passar o tempo de timeout
                threading.Thread(target=pendingTimeout, args=(self.timeout, self.pendingTable, (directive,'ROUTE_REPLY'),)).start()

                print('[ROUTE_REQUEST] forward')

        elif pdu_type == 'ROUTE_REPLY':
            row = directive.split(' ')
            if self.pendingTable.check((row[0], 'ROUTE_REPLY')):
                faces = self.pendingTable.get((row[0], 'ROUTE_REPLY'))
                self.pendingTable.rm((row[0], 'ROUTE_REPLY'))
                if self.name in faces:
                    self.routingTable.addNode(row[0], source, row[1], time.time())
                    faces.remove(self.name)
                    print('[ROUTE_REPLY] tabela de routing atualizada')
                
                if faces != []:
                    self.routingTable.addNode(row[0], source, row[1], time.time())
                    newpdu = PDU('ROUTE_REPLY', self.name, faces[0], self.radius, None, directive, [self.name])
                    print('[ROUTE_REPLY] forward')

        elif pdu_type == 'CONTENT_REQUEST':
            if self.contentStore.checkContent(directive):
                strrow = directive + ' ' + self.contentStore.getContent(directive)
                newpdu = PDU('CONTENT_REPLY', self.name, source, self.radius, None, strrow, [self.name])
                print('[CONTENT_REQUEST] found')
            elif self.pendingInterestTable.check(directive):
                self.pendingInterestTable.add(directive, source)
                print('[CONTENT_REQUEST] already requested')
            else:
                self.pendingInterestTable.add(directive, source)
                newpdu = PDU('CONTENT_REQUEST', source, None, ttl-1, None, directive, [self.name])

                # Criar thread para remover elemento da pendingTable depois do passar o tempo de timeout
                threading.Thread(target=pendingTimeout, args=(self.timeout, self.pendingInterestTable, (directive, 'CONTENT_REPLY'),)).start()

                print('[CONTENT_REQUEST] forward')

        elif pdu_type == 'CONTENT_REPLY':
            row = directive.split(' ')
            if self.pendingInterestTable.check(row[0]):
                faces = self.pendingInterestTable.get(row[0])
                self.pendingInterestTable.rm(row[0])
                if self.name in faces:
                    self.contentStore.addContent(row[0], row[1])
                    faces.remove(self.name)
                    print('[CONTENT_REPLY] tabela de routing atualizada')
                    print('-----------------------')
                    print('Content | Value ')
                    content = self.contentStore.getContent(row[0])
                    print(row[0], '  ', content)
                    print('-----------------------')
                
                if faces != []:
                    self.contentStore.addContent(row[0], row[1])
                    newpdu = PDU('CONTENT_REPLY', self.name, faces[0], self.radius, None, directive, [self.name])
                    print('[CONTENT_REPLY] forward')

        elif pdu_type == 'TARGET_REQUEST':
            if target == self.name:
                strrrow = directive + ' ' + self.contentStore.getContent(directive)
                newpdu = PDU('TARGET_REPLY', self.name, source, self.radius, None, strrow, [self.name])
                print('[TARGET_REQUEST] found')
            elif self.routingTable.exists(target):
                newpdu = PDU('TARGET_REQUEST', source, target, ttl-1, None, directive, [self.name])
                print('[TARGET_REQUEST] forward')

        elif pdu_type == 'TARGET_REPLY':
            row = directive.split(' ')
            if target == self.name:
                self.pendingInterestTable.rm(row[0])
                self.contentStore.addContent(row[0], row[1])
                print('-----------------------')
                print('Content | Value ')
                content = self.contentStore.getContent(row[0])
                print(row[0], '  ', content)
                print('-----------------------')
                print('[TARGET_REPLY] found')
            else self.routingTable.exists(target):
                self.contentStore.addContent(row[0], row[1])
                newpdu = PDU('TARGET_REPLY', source, target, ttl-1, None, directive, [self.name])
                print('[TARGET_REPLY] forward')
        else:
            print('[PDU TYPE unknown]', pdu_type)


        return newpdu