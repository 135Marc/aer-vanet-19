
class Table:
    fields = ['Nome', 'Vizinho', 'Endereço do vizinho']
    rows = set()

    def addNode(self, nome, vizinho, endereco):
        row = (nome, vizinho, endereco)
        self.rows.add(row)

    def printTable(self):
        print('-------------------------------------')
        print(self.fields[0] + ' | ' + self.fields[1] + ' | ' + self.fields[2])
        for i in range(0, len(self.nomes)-1):
            print(self.rows[i][0] + '   |   ' + self.vizinhos[i][1] + '   |   ' + self.enderecos[i][2])
        print('-------------------------------------')
