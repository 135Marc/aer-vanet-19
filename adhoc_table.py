import time

class Table:
    fields = ['Nome', 'Vizinho', 'Endereço do vizinho']
    rows = set()
    neighbours = set()

    def __init__(self, givenRows = set(), givenNeighbours = set()):
        self.rows = givenRows.copy()
        self.neighbours = givenNeighbours.copy()

    def addNode(self, nome, vizinho, endereco, time):
        #Verificar se o nodo já está na tabela (caso esteja na tabela será removido)
        rmrow = None
        for row in self.rows:
            if (row[0] == nome) & (nome == vizinho):
                rmrow = (row[0], row[1], row[2], row[3])
        if rmrow:
            self.rows.remove(rmrow)
        #Adicionar o nodo há tabela
        newrow = (nome, vizinho, endereco, time)
        self.rows.add(newrow)

    def addNeighbour(self, nome, vizinho, endereco, time):
        #Verificar se o vizinho já existe (caso exista será removido)
        rmrow = None
        for row in self.neighbours:
            if (row[0] == nome) & (nome == vizinho):
                rmrow = (row[0], row[1], row[2], row[3])
        if rmrow:
            self.neighbours.remove(rmrow)
        #Adicionar o novo vizinho
        row = (nome, vizinho, endereco, time)
        self.neighbours.add(row)

    def getRows(self):
        return self.rows

    def getNeighbours(self):
        return self.neighbours

    def mergeTable(self, table, source, time, this):
        #Descobrir nodos de nivel dois que ainda não existem
        actual_nodes = set()
        incoming_nodes = set()
        for node in self.rows:
            actual_nodes.add(node[0])
        for node in table.getNeighbours():
            incoming_nodes.add(node[0]) 
        toadd_nodes = incoming_nodes - actual_nodes
        toadd.remove(this)

        #Adicionar nodos de nivel dois que ainda não existem
        for node in toadd_nodes:
            for row in table.getRows():
                if(row[0] == node): 
                    self.rows.add((row[0], source, row[2], time))

        #Atualizar o timestamp dos vizinhos deste nodo
        toup_nodes = set()         
        for row in self.rows:
            if row[1] == source:
                toup_nodes.add(row)
        for node in toup_nodes:        
            self.rows.remove(node)
            self.rows.add((node[0], node[1], node[2], time))

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
        print(self.fields[0] + ' | ' + self.fields[1] + ' | ' + self.fields[2])
        for node in self.rows:
            print(node[0] + '    |    ' + node[1] + '    |   ' + node[2])
        print('-------------------------------------')


            