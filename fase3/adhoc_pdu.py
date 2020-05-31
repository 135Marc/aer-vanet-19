from adhoc_table import Table

class PDU:
    pdu_type = ''
    source = 'None'
    target = 'None'
    ttl = 0
    table = None
    directive = 'None'
    path = []

    def __init__(self, pdu_type, source, target, ttl, table, directive, path):
        self.pdu_type = pdu_type 
        self.source = source
        self.target = target
        self.ttl = ttl
        if table:
            self.table = Table(table.getRows(), table.getNeighbours())
        self.directive = directive
        self.path = []
        for n in path:
            self.path.append(n)

    def getType(self):
        return self.pdu_type
    def getSource(self):
        return self.source
    def getTarget(self):
        return self.target
    def getTTL(self):
        return self.ttl
    def getTable(self):
        return self.table
    def getDirective(self):
        return self.directive
    def getPath(self):
        pathcopy = []
        for n in self.path:
            pathcopy.append(n)
        return pathcopy

    def printPDU(self):
        print('**************************')
        print('PDU type:', self.pdu_type)
        print('Source:', self.source)
        print('Target:', self.target)
        print('TTL:', str(self.ttl))
        print('Directive:', self.directive)
        print('Path:', ','.join(self.path))
        print('**************************')