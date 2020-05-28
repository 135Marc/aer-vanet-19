
class PendingInterestTable:
    tableOfPendingInterest = {
        'default/interest': ['A'] 
    }

    def checkInterest(self, name):
        return name in self.tableOfPendingInterest

    def addInterest(self, name, source):
        if name in self.tableOfPendingInterest:
            self.tableOfPendingInterest[name].append(source)
        else:
            self.tableOfPendingInterest[name] = [source]

    def getInterested(self, name):
        return self.tableOfPendingInterest[name]

    def rmInterest(self, name):
        del tableOfPendingInterest[name]