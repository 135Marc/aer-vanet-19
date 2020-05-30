import time

class Table:
    fields = ['Face', 'Vizinho', 'Content', 'Timestamp']
    rows = set()
    neighbours = set()

    def __init__(self, givenRows = set(), givenNeighbours = set()):
        self.rows = givenRows.copy()
        self.neighbours = givenNeighbours.copy()

    def addNode(self, nome, vizinho, content, timestamp):
        #Verificar se o no já está na tabela (caso esteja na tabela será removido)
        rmrow = None
        for row in self.rows:
            if row[0] == nome:
                rmrow = (row[0], row[1], row[2], row[3])
        if rmrow:
            self.rows.remove(rmrow)
        #Adicionar o nodo há tabela
        newrow = (nome, vizinho, content, timestamp)
        self.rows.add(newrow)

    def addNeighbour(self, nome, endereco, timestamp):
        #Verificar se o vizinho já existe (caso exista será removido)
        rmrow = None
        for row in self.neighbours:
            if row[0] == nome:
                rmrow = (row[0], row[1], row[2], row[3])
        if rmrow:
            self.neighbours.remove(rmrow)
        #Adicionar o novo vizinho
        row = (nome, nome, endereco, timestamp)
        self.neighbours.add(row)

    def mergeTable(self, zone, source, name, table, timestamp):
        # Descobrir nodos de nivel dois que ainda não existem
        actual_nodes = set()
        incoming_nodes = set()
        for node in self.rows:
            actual_nodes.add((node[0], node[2]))
        for node in table.getNeighbours():
            incoming_nodes.add((node[0], node[2]))

        # Nos para adicionar
        toadd_nodes = incoming_nodes - actual_nodes

        # Remover este mesmo nodo da lista de nodos a adicionar
        toadd_nodes.discard((name, zone))

        #Adicionar nodos de nivel dois que ainda não existem
        for node in toadd_nodes:
            self.rows.add((node[0], source, node[1], timestamp))

    def verifyTimes(self, dead_imterval):
        actual_time = time.time()
        rmset = set()
        for row in self.rows:
            if actual_time - row[3] > dead_imterval:
                rmset.add(row)
                
        self.neighbours.difference_update(rmset)
        self.rows.difference_update(rmset)
    
    def getRows(self):
        return self.rows

    def getNeighbours(self):
        return self.neighbours

    def exists(self, nodo):
        newnode = None
        for row in self.rows:
            if row[0] == nodo:
                newnode = row
        return newnode

    def remove(self, nodo):   
        newnode = None 
        for row in self.rows:
            if row[0] == nodo:
                newnode = row
        if newnode:
            self.rows.remove(newnode)

    def printTable(self):
        print('-------------------------------------')
        print(self.fields[0] + ' | ' + self.fields[1] + ' | ' + self.fields[2])
        for node in self.rows:
            print(node[0] + '    |    ' + node[1] + '    |   ' + node[2])
        print('-------------------------------------')

    def getStr(self):
        string = '-------------------------------------\n'
        string += self.fields[0] + ' | ' + self.fields[1] + ' | ' + self.fields[2] + '\n'
        for node in self.rows:
            string += node[0] + '    |    ' + node[1] + '    |   ' + node[2] + '\n'
        string += '-------------------------------------'

        return string

            