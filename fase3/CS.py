
class ContentStore:
    tableOfContents = {
        'default/state': 'CS inicial state.' 
    }

    def __init__(self, zone):
        self.tableOfContents[zone] = 'oficial' + zone

    def checkContent(self, name):
        return name in self.tableOfContents

    def addContent(self, name, value):
        if not name in self.tableOfContents:
            self.tableOfContents[name] = value

    def getContent(self, name):
        return self.tableOfContents[name]

    def printCS(self):
        print('--------Contents-------')
        for k in self.tableOfContents.keys():
            print(k)
        print('-----------------------')


        