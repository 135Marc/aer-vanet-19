
class PendingInterestTable:
    tableOfPendingInterest = {
        'default/interest': ['A'] 
    }

    def check(self, name):
        return name in self.tableOfPendingInterest

    def add(self, name, source):
        if name in self.tableOfPendingInterest:
            self.tableOfPendingInterest[name].append(source)
        else:
            self.tableOfPendingInterest[name] = [source]

    def get(self, name):
        return self.tableOfPendingInterest[name]

    def rm(self, name):
        del self.tableOfPendingInterest[name]