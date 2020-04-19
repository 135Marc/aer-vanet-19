
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
        print(fields[0] + '|' + fields[1] + '|' + fields[2])
        for i in range(0, len(nomes)):
            print(nomes[i] + '|' + vizinhos[i] + '|' + enderecos[i])
        print('-------------------------------------')
