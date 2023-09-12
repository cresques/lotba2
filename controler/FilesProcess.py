import os
from controler.AppData import AppData
from controler.FilesStats import FilesStats

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class FilesProcess(Singleton, FilesStats):
    def __init__(self):
        FilesStats.__init__(self)
        self.doInsert = False
        self.__loadedFilesDuplicatedControl = []

    def getProcess(self):
        return self.__instance

    def getMeses(self):
        ret = []
        for m in ("209", "210", "211", "212", "301", "302", "303"):
            ret += ["202%s" % m]
        return ret

    def getFNames(self, dName, mes):
        fNames = []
        for fName in os.listdir("%s/%s" % (AppData.dataDir, dName)):
            if ".xml" in fName and mes in fName:
                fNames += [fName]
        return fNames

    def addFileToControl(self, f):
        self.__loadedFilesDuplicatedControl.append(f)

    def isFileInControl(self, f):
        return f in self.__loadedFilesDuplicatedControl
