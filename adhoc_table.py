
class Table:
    fields = ['Nome', 'Vizinho', 'Endereço do vizinho']
    rows = set()

    def __init__(self, givenRows = set()):
        self.rows = givenRows.copy()

    def addNode(self, nome, vizinho, endereco):
        row = (nome, vizinho, endereco)
        self.rows.add(row)

    def getRows(self):
        return self.rows

    def mergeTable(self, table):
        actual_nodes = set()
        incoming_nodes = set()
        for node in self.rows:
            actual_nodes.add(node[0])
        for node in table.getRows():
            incoming_nodes.add(node[0])

        toadd_nodes = incoming_nodes - actual_nodes
        for node in toadd_nodes:
            for row in table.getRows():
                if(row[0] == node): 
                    self.rows.add(row)

    def printTable(self):
        print('-------------------------------------')
        print(self.fields[0] + ' | ' + self.fields[1] + ' | ' + self.fields[2])
        for node in self.rows:
            print(node[0] + '    |    ' + node[1] + '    |   ' + node[2])
        print('-------------------------------------')


            