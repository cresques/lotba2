
class Stats():
    dict = {}

    def __init__(self):
        self.dict = {}
        self.dict['FieldError'] = {}
        self.dict['FileError'] = []

    def addFieldError(self, label):
        #print("Stats.addFieldError(): %s" % label)
        if not label in self.dict['FieldError'].keys():
            self.dict['FieldError'][label] = 0
        self.dict['FieldError'][label] += 1

class XmlFile:
    fName = ""
    def __init__(self, fName):
        self.fName = fName
        self.stats = Stats()
        self.debug = False

    def setStat(self, k, v):
        self.stats.dict[k] = v

    def getStat(self, k):
        if k in self.stats.dict.keys():
            return self.stats.dict[k]
        return None

    def addFileError(self, lbl):
        self.stats.dict["FileError"].append(lbl)

    def addFieldError(self, lbl):
        self.stats.addFieldError(lbl)

    def parseFile(self):
        pass

    def getDataByTagName(self, element, tagName, default=None):
        func="XmlFile.getDataByTagName()"
        ret = default
        try:
            ret = element.getElementsByTagName(tagName)[0].firstChild
            if ret is not None:
                ret = ret.data
            else:
                ret = ""
        except IndexError:
            if self.debug:
                print("ERROR %s: No tiene %s " % (func, tagName))
            self.addFieldError(tagName)

        return ret

