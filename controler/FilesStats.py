

class FilesStats():
    """
    Statistics class for RUProcess
    """
    __rudFilesDict = {}
    __rudDataDict = {}
    def __init__(self):
        self.__rudFilesDict = {}
        self.__rudDataDict = {}

    def addFile(self, fName, rudFile):
        self.__rudFilesDict[fName] = rudFile

    def addData(self, fName, rudData):
        self.__rudDataDict[fName] = rudData

    def contains(self, fName):
        return fName in self.__rudDataDict.keys()

    def getStats(self, fName):
        rudF = self.__rudFilesDict[fName]
        if fName in self.__rudDataDict:
            rudD = self.__rudDataDict[fName]
        else:
            rudD = None

        ret = {}
        ret["numJugadores"] = rudF.getStat("numJugadores")
        ret["numEstados"] = rudF.getStat("numEstados")
        ret["errors"] = rudF.getStat("FileError")
        if rudD is not None:
            ret["errors"] += rudD.getStat("Error")

        return ret

    def getErrors(self):
        msg = []
        for d in self.__rudDataDict:
            e = d.getStats['Error']
            for m in e:
                msg += [m]
        return msg

