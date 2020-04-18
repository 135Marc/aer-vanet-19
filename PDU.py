
class PDU:

    pdu_type = "HELLO"
    ttl = 1
    def __init__(self, givenType, givenTTL):
        self.pdu_type = givenType 
        self.ttl = givenTTL

    def getType(self):
        return self.pdu_type

    def getTTL(self):
        return self.ttl

    def setType(self, givenType):
        self.pdu_type = givenType

    def setTTL(self, givenTTL):
        self.ttl = givenTTL

    