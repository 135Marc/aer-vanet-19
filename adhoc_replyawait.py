
class ReplyWait:
    awaiting = []

    def __init__(self, givenAwaiting=[]):
        for n in givenAwaiting:
            self.awaiting.append(n)

    def checkElem(self, elem):
        return (elem in self.awaiting)

    def addElem(self, n):
        self.awaiting.append(n)

    def rmElem(self, n):
        self.awaiting.remove(n)

    def printReplyWait(self):
        print('**************************')
        print('* Waiting: ' + ', '.join(list(self.awaiting)))
        print('**************************')