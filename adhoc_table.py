
class Table:
    fields = ['Nome', 'Vizinho', 'Endereço do vizinho']
    nomes = []
    vizinhos = []
    enderecos = []

    def addNode(self, nome, vizinho, endereco):
        self.nomes.append(nome)
        self.vizinhos.append(vizinho)
        self.enderecos.append(endereco)

    def printTable(self):
        print('-------------------------------------')
        print(self.fields[0] + '      |' + self.fields[1] + '      |' + self.fields[2])
        for i in range(0, len(self.nomes)):
            print(self.nomes[i] + '      |' + self.vizinhos[i] + '      |' + self.enderecos[i])
        print('-------------------------------------')
