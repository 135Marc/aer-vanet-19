
from adhoc_table import Table

class PDU:
    source = 'None'
    pdu_type = "HELLO"
    ttl = 1
    table = None
    target = 'None'
    msg = ''
    path = []

    def __init__(self, givenSource, givenType, givenTTL, givenTable, givenTarget='None', givenMSG='', givenPath=[]):
        self.source = givenSource
        self.pdu_type = givenType 
        self.ttl = givenTTL
        if givenType == 'HELLO':
            self.table = Table(givenTable.getRows(), givenTable.getNeighbours())
        if givenType == 'ROUTE_REQUEST' or givenType == 'ROUTE_REPLY':
            self.target = givenTarget
            self.msg = givenMSG
            for n in givenPath
                self.path.append(n)

    def getSource(self):
        return self.source
    def getType(self):
        return self.pdu_type
    def getTTL(self):
        return self.ttl
    def getTable(self):
        return self.table
    def getTarget(self):
        return self.target
    def getMsg(self):
        return self.msg
    def getPath(self):
        return self.path

    def setSource(self, givenSource):
        self.source = givenSource
    def setType(self, givenType):
        self.pdu_type = givenType
    def setTTL(self, givenTTL):
        self.ttl = givenTTL
    def setTable(self, givenTable):
        self.table = Table(givenTable.getRows(), givenTable.getNeighbours())
    def setTarget(self, givenTarget):
        self.target = givenTarget
    def setMsg(self, givenMsg):
        self.msg = givenMsg

    def replyPDU(self, n, t, m):
        self.source = n
        self.pdu_type = 'ROUTE_REPLY'
        self.ttl = 10
        self.target = t
        self.msg = m

    def forwardingPDU(self, node):
        self.ttl -= 1
        if self.pdu_type == 'ROUTE_REQUEST':
            self.path.append(node)
        if self.pdu_type == 'ROUTE_REPLY':
            self.path.pop(node)

    def printPDU(self):
        print('**************************')
        print('* Source: ' + self.source)
        print('* PDU type: ' + self.pdu_type)
        print('* TTL: ' + str(self.ttl))
        print('* Target: ' + self.target)
        print('* Msg: ' + self.msg)
        print('* Path: ' + ', '.join(list(self.path)))
        print('**************************')