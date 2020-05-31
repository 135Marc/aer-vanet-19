
class ContentStore:
    tableOfContents = {
        'default/state': 'CS inicial state.' 
    }

    def checkContent(self, name):
        return name in self.tableOfContents

    def addContent(self, name, value):
        self.tableOfContents[name] = value

    def getContent(self, name):
        return self.tableOfContents[name]

    def printCS(self):
        print('---------------Contents-----------------')
        for k in self.tableOfContents.keys():
            print(k)
        print('-------------------------------------')


        