
class Table:
    fields = ['Nome', 'Vizinho', 'Endereço do vizinho']
    rows = set()

    def addNode(self, nome, vizinho, endereco):
        row = (nome, vizinho, endereco)
        self.rows.add(row)

    def printTable(self):
        print('-------------------------------------')
        print(self.fields[0] + ' | ' + self.fields[1] + ' | ' + self.fields[2])
        for node in self.rows):
            print(node[0] + '   |   ' + node[1] + '   |   ' + node[2])
        print('-------------------------------------')
