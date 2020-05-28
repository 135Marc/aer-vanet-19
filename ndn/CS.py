
class ContentStore:
    tableOfContents = {
        'default/state': 'CS inicial state.' 
    }

    def checkContent(self, name):
        return name in self.tableOfContents

    def addContent(self, name, value):
        self.tableOfContent[name] = value

    def getContent(self, name):
        return self.tableOfContent[name]

        