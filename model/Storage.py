

class Stats():
    __statsDict = {}
    def __init__(self):
        self.__statsDict = {}
        self.setStat('Error', [])

    def addError(self, msg):
        e = self.getStat('Error')
        e += [msg]
        self.setStat('Error', e)

    def setStat(self, k, v):
        self.__statsDict[k] = v

    def getStat(self, k):
        if k in self.__statsDict.keys():
            return self.__statsDict[k]
        return None
