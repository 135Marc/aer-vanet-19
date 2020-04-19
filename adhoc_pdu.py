
class PDU:
    node = 'NaN'
    pdu_type = "HELLO"
    ttl = 1
    
    def __init__(self, givenNode, givenType, givenTTL):
        self.node = givenNode
        self.pdu_type = givenType 
        self.ttl = givenTTL

    def getNode(self):
        return self.node

    def getType(self):
        return self.pdu_type

    def getTTL(self):
        return self.ttl

    def setNode(self, givenNode):
        self.node = givenNode

    def setType(self, givenType):
        self.pdu_type = givenType

    def setTTL(self, givenTTL):
        self.ttl = givenTTL

    