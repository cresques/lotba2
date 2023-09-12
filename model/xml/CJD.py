import xml.dom.minidom
from model.xml.XmlFile import XmlFile

class CJD(XmlFile):
    def __init__(self, fName):
        #super.__init__(self, fName)
        self.fName = fName

    def parseFile(self):
        doc = xml.dom.minidom.parse(self.fName)
        print(doc.nodeName)
        print(doc.firstChild.tagName)

        for tagName in ("Registro","Jugador"):
            #tagName = "Jugador"
            tag = doc.getElementsByTagName(tagName)
            print("%d %s:" % (tag.length, tagName))