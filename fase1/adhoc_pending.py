
class Pending:
    pendingTable = { 
    }

    def check(self, targettype):
        return targettype in self.pendingTable

    def add(self, targettype, source):
        if targettype in self.pendingTable:
            self.pendingTable[targettype].append(source)
        else:
            self.pendingTable[targettype] = [source]

    def get(self, targettype):
        return self.pendingTable[targettype]

    def rm(self, targettype):
        del self.pendingTable[targettype]