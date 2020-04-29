
from adhoc_table import Table

class PDU:
    source = 'None'
    pdu_type = "HELLO"
    ttl = 1
    table = None
    target = 'None'
    path = []

    def __init__(self, givenSource, givenType, givenTTL, givenTable, givenTarget='None', givenPath=[]):
        self.source = givenSource
        self.pdu_type = givenType 
        self.ttl = givenTTL
        self.table = Table(givenTable.getRows(), givenTable.getNeighbours())
        if givenType == 'ROUTE_REQUEST':
            self.target = givenTarget
            self.path = givenPath

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

    def printPDU(self):
        print('Source: ' + self.source)
        print('PDU type: ' + self.pdu_type)
        print('TTL: ' + str(self.ttl))
        print('Target: ' + self.target)