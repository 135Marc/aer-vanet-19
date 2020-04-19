
class PDU:
    source = 'NaN'
    pdu_type = "HELLO"
    ttl = 1
    
    def __init__(self, givenSource, givenType, givenTTL):
        self.source = givenSource
        self.pdu_type = givenType 
        self.ttl = givenTTL

    def getSource(self):
        return self.source

    def getType(self):
        return self.pdu_type

    def getTTL(self):
        return self.ttl

    def setSource(self, givenSource):
        self.source = givenSource

    def setType(self, givenType):
        self.pdu_type = givenType

    def setTTL(self, givenTTL):
        self.ttl = givenTTL

    