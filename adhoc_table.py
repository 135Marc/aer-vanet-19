import time

class Table:
    fields = ['Nome', 'Vizinho', 'Endereço do vizinho']
    rows = set()
    neighbours = set()

    def __init__(self, givenRows = set(), givenNeighbours = set()):
        self.rows = givenRows.copy()
        self.neighbours = givenNeighbours.copy()

    def addNode(self, nome, vizinho, endereco, time = time.time()):
        rmrow = None
        for row in self.rows:
            if (row[0] == nome) & (nome == vizinho):
                rmrow = (row[0], row[1], row[2], row[3])
        if rmrow:
            self.rows.remove(rmrow)
        newrow = (nome, vizinho, endereco, time)
        self.rows.add(newrow)

    def addNeighbour(self, nome, vizinho, endereco, time = time.time()):
        row = (nome, vizinho, endereco, time)
        self.neighbours.add(row)

    def getRows(self):
        return self.rows

    def getNeighbours(self):
        return self.neighbours

    def mergeTable(self, table, source, time = time.time()):
        actual_nodes = set()
        incoming_nodes = set()
        for node in self.rows:
            actual_nodes.add(node[0])
        for node in table.getNeighbours():
            incoming_nodes.add(node[0])

        toadd_nodes = incoming_nodes - actual_nodes
        for node in toadd_nodes:
            for row in table.getRows():
                if(row[0] == node): 
                    self.rows.add((row[0], source, row[2], time))

    def verifyTimes(self, interval):
        actual_time = time.time()
        rmset = set()
        for row in self.rows:
            if row[3] != 0:
                if actual_time - row[3] > interval:
                    rmset.add(row)
        self.neighbours.difference_update(rmset)
        self.rows.difference_update(rmset)

    def printTable(self):
        print('-------------------------------------')
        print(self.fields[0] + ' | ' + self.fields[1] + ' | ' + self.fields[2]+ ' | ' + 'time')
        for node in self.rows:
            print(node[0] + '    |    ' + node[1] + '    |   ' + node[2] + '    |   ' + str(node[3]))
        print('-------------------------------------')


            