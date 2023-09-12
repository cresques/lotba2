import os, locale #, json
from datetime import datetime
from model.xml.CJD import CJD
from model.xml.RUD import RUD
from model.db.mysql.TestDB import TestDB
from controler.AppData import AppData
from controler.AppStart import AppStart
from controler.RU.RUProcess import RUDProcess

class lotba():
    dataDir = "/LOTBA"
    msg = []
    def __init__(self, dataDir = "/LOTBA"):
        #self.open(dataDir)
        pass

    def open(self, dataDir = "/LOTBA"):
        self.dataDir = dataDir
        dbName = "LOTBA3"
        print("LOTBA file load starting in %s...\n" % dbName)
        AppData("C:\\Users\\luis.sevilla\\projects\\lotba-xml\\LOTBA", dbName)

    def close(self):
        print("LOTBA: ending in %s...\n" % AppData.db.dbName)

    def cleanMsg(self):
        self.msg = []

    def addMsg(self, msg):
        self.msg.append(msg)

    def printMsg(self):
        for msg in self.msg:
            print(msg)

    def testXmlCJD(self, dName, fName):
        self.dName = dName
        self.fName = fName
        cjd = CJD("%s/%s/%s" % (self.dataDir, dName, fName))
        cjd.parseFile()

    def testXmlRUD(self, dName, fName):
        self.dName = dName
        self.fName = fName
        rudFile = RUD("%s/%s/%s" % (self.dataDir, dName, fName))
        rudFile.parseFile()
        print("%d jugadores en '%s'" % (len(rudFile.jugadores), fName))
        return rudFile

    def testXml1(self):
        #dName, fName = "AJL0005\\CJ\\Diario\\CJD", "AJL0005_AJL0005_SCI_CJ_CJD_D_20230101_ALI188401.xml"
        #app.testXmlCJD(dName, fName)
        dName = "AJL0005\\RU\\Diario\\RUD"
        fNames = [
 #           "AJL0005_AJL0005_SCI_RU_RUD_D_20230101_ALI188379.xml",
            "AJL0005_AJL0005_SCI_RU_RUD_D_20230102_ALI189350.xml",
 #           "AJL0005_AJL0005_SCI_RU_RUD_D_20230103_ALI190316.xml",
 #           "AJL0005_AJL0005_SCI_RU_RUD_D_20230104_ALI191282.xml"
            ]
        self.jugadoresDia = []
        for fName in fNames:
            self.jugadoresDia.append(self.testXmlRUD(dName, fName).jugadores)

    def testDB1(self):
        db3 = TestDB()
        db3.testCab("LOTBA3")
        db3.showColumns("RUD_D_Estado")

        #db2 = TestDB()
        #db2.testCab("LOTBA")
        #db2.selectRUD_D()

    def getFNames(self, dName, mes):
        fNames = []
        for fName in os.listdir("%s/%s" % (self.dataDir, dName)):
            if ".xml" in fName and mes in fName:
                fNames += [fName]
        return fNames

    def testXmlaDB_RUD_M(self):
        func = "%s.testXmlaDB_RUD_M" % self.__class__.__name__
        dName = "AJL0005/RU/Mensual/RUD"
        t1 = datetime.now()

        fNames = self.getFNames(dName, "202301")

        '''fNames = [
            "AJL0005_AJL0005_SCI_RU_RUD_D_20230101_ALI188379.xml",
            "AJL0005_AJL0005_SCI_RU_RUD_D_20230102_ALI189350.xml",
            "AJL0005_AJL0005_SCI_RU_RUD_D_20230103_ALI190316.xml",
            "AJL0005_AJL0005_SCI_RU_RUD_D_20230104_ALI191282.xml"
        ]'''
        db3 = TestDB()
        db3.testCab("LOTBA3")
        for fName in fNames:
            j = self.testXmlRUD(dName, fName).jugadores
            db3.testInsertRUD_M(j)
        db3.conn.appClose()
        t2 = datetime.now()
        t = t2 - t1
        print("INFO %s: %s Time elapsed %s." % (func, t2.strftime("%d/%m/%Y %H:%M:%S"), t))

    def testLoadRUD_D(self, mes):
        func = "%s.testLoadRUD_D()" % self.__class__.__name__
        t1 = datetime.now()
        proc = RUDProcess()
        proc.doInsert = True
        proc.loadXmltoRUD_DMes(mes)
        t2 = datetime.now()
        t = t2 - t1
        self.addMsg("INFO %s: %s Time processing %7s Jugadores in RUD_D XML for %s: %s." %
              (func, t2.strftime("%d/%m/%Y %H:%M:%S"), f"{proc.jugadoresCnt:n}", mes, t))

    def testLoadRUD_M(self, mes):
        func = "%s.testLoadRUD_M()" % self.__class__.__name__
        t1 = datetime.now()
        proc = RUDProcess()
        proc.doInsert = True
        proc.loadXmltoRUD_MMes(mes)
        t2 = datetime.now()
        t = t2 - t1
        self.addMsg("INFO %s: %s Time processing %7s Jugadores in RUD_M XML for %s: %s." %
              (func, t2.strftime("%d/%m/%Y %H:%M:%S"), f"{proc.jugadoresCnt:n}", mes, t))

    def testLoadRUD_MTodo(self):
        func = "%s.testLoadRUD_MTodo()" % self.__class__.__name__
        for m in ["208", "209", "210", "211", "212", "301"]:
            mes = "202%s" % m
            self.testLoadRUD_M(mes)

    def showColumns(self, tName="RUD_M"):
        """
        Lista por consola las columnas de una tabla
        :param tName: Nombre de la tabla
        :return:
        """
        AppData.db.showColumns(tName)

    def showDBErrors(self):
        func = "%s.showDBErrors()" % self.__class__.__name__
        self.cleanMsg()
        self.addMsg("\nINFO %s:   DB Errors: " % func)
        for msg in AppData.db.getDbErrors():
            self.addMsg(msg)
        self.printMsg()

def runLotba():
    func = "runLotba()"
    locale.setlocale(locale.LC_ALL, 'es_ES')
    t1 = datetime.now()
    app = lotba()
    app.open()
    #mes = "202301"
    app.cleanMsg()
    app.addMsg("\nINFO %s:   Summary: " % func)
    #app.showColumns("RUD_M")
    #app.testLoadRUD_D("202301")
    #app.testLoadRUD_M("202301")
    #app.printMsg()
    #app.showDBErrors()
    for table in ("RUT_D","RUT_D_NumeroApostadoresPorEstado","RUT_M","RUT_M_NumeroApostadoresPorEstado"):
        app.showColumns(table)
    t2 = datetime.now()
    t = t2 - t1
    print("\nINFO %s: %s Total running time: %s." %
        (func, t2.strftime("%d/%m/%Y %H:%M:%S"), t))
    app.close()

def tablesJson():
    TestDB().tables_json()
    exit()

if __name__ == '__main__':
    #tablesJson()

    web = False
    if not web:
        AppStart().start()
        #runLotba()
    else:
        AppStart().webStart()

