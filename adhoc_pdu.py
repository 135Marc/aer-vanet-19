
from adhoc_table import Table

class PDU:
    source = 'NaN'
    pdu_type = "HELLO"
    ttl = 1
    table = None

    def __init__(self, givenSource, givenType, givenTTL, givenTable):
        self.source = givenSource
        self.pdu_type = givenType 
        self.ttl = givenTTL
        self.table = Table(givenTable.getRows(), givenTable.getNeighbours())

    def getSource(self):
        return self.source
    def getType(self):
        return self.pdu_type
    def getTTL(self):
        return self.ttl
    def getTable(self):
        return self.table

    def setSource(self, givenSource):
        self.source = givenSource
    def setType(self, givenType):
        self.pdu_type = givenType
    def setTTL(self, givenTTL):
        self.ttl = givenTTL
    def setTable(self, givenTable):
        self.table = givenTable

    