
class ForwardingInformationBase:
    tableOfForwardingInformation = {
        'base/name': ['C'] 
    }

    def checkInterface(self, name):
        return name in self.tableOfForwardingInformation

    def addInterface(self, name, interface):
        if name in self.tableOfForwardingInformation:
            self.tableOfForwardingInformation[name].append(interface)
        else:
            self.tableOfForwardingInformation[name] = [interface]

    def getInterfaces(self, name):
        return tableOfForwardingInterest[name]