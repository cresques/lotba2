import os
from datetime import datetime
from controler.AppData import AppData
from controler.FilesProcess import FilesProcess
from model.xml.RUD import RUD
from model.db.mysql.RU.RUD_D import RUD_D
from model.db.mysql.RU.RUD_M import RUD_M
'''
class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class RUProcess(Singleton, FileStats):
    def __init__(self):
        FileStats.__init__(self)
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
'''
class RUDProcess(FilesProcess):

    def __init__(self, dirDiario="AJL0005/RU/Diario/RUD", dirMensual="AJL0005/RU/Mensual/RUD"):
        FilesProcess.__init__(self)
        """
        Procesa ficheros XML y los inserta en la BBDD Lotba
        :param dirDiario: directorio de los ficheros xml diarios
        :param dirMensual: directorio de los ficheros xml mensuales
        """
        self.doInsert = False
        self.dDName = dirDiario
        self.dMName = dirMensual

    def readXmlRUDFile(self, dName, fName):
        self.dName = dName
        self.fName = fName
        rudFile = RUD("%s/%s/%s" % (AppData.dataDir, dName, fName))
        rudFile.debug = False
        rudFile.parseFile()
        self.addFile(fName, rudFile)
        return rudFile

    def insertJugadoresRUD_D(self, jugadores, fName):
        func="%s.insertJugadoresRUD_D()" % self.__class__.__name__
        t1 = datetime.now()
        print("DEBUG %s: Insertando jugadores en RUD_D" % func)
        rudd = RUD_D(AppData.db)
        jj = jugadores  # [:10]
        doInsertAll=True
        if doInsertAll:
            print("DEBUG %s: Inserto %d jugadores" % (func, len(jj)))
            rudd.insertJugadoresRud(jugadores, fName)
            rudd.insertEstadosRud(jugadores, fName)
        else:
            for jugador in jj:
                print("DEBUG %s: Inserto jugador id='%s' ..." % (func, jugador.jugadorId))
                rudd.insertJugadorRud(jugador)
        rudd.conn.commit()
        self.addData(fName, rudd)
        # rudd.conn.close()
        t2 = datetime.now()
        t = t2 - t1
        print("INFO %s: %s Time elapsed %s." % (func, t2.strftime("%d/%m/%Y %H:%M:%S"), t))
        return rudd

    def getRUD_DFNames(self, dName = "AJL0005/RU/Diario/RUD", mes='202302'):
        return self.getFNames(dName, mes)

    def loadXmltoRUD_DFile(self, fName):
        func="%s.loadXMLtoRUD_DFile()" % self.__class__.__name__
        print("INFO %s: loading %s ..." % (func, fName))
        t1 = datetime.now()
        rudFile = self.readXmlRUDFile(self.dDName, fName)
        rudData = None
        j = rudFile.jugadores
        f = (len(j),rudFile.getStat("numEstados"))
        if not self.isFileInControl(f):
            self.addFileToControl(f)
            print("INFO %s: %d jugadores en '%s'" % (func, f[0], fName))
            if self.doInsert:
                rudData = self.insertJugadoresRUD_D(j, fName)
        else:
            errMsg = "Datos duplicados"
            rudFile.addFileError(errMsg)
            print("ERROR %s: %d jugadores en '%s'. %s" % (func, f[0], fName, errMsg))
        t2 = datetime.now()
        t = t2-t1
        print("INFO %s: %s Time processing %d Jugadores in RUD_D XML: %s." %
              (func, t2.strftime("%d/%m/%Y %H:%M:%S"), f[0], t))
        return (rudFile, rudData)

    def loadXmltoRUD_DMes(self, mes="202301"):
        func="%s.loadXMLtoRUD_DMes()" % self.__class__.__name__
        t1 = datetime.now()
        self.loadedFilesDuplicatedControl = []
        fNames = self.getRUD_DFNames(self.dDName, mes)

        self.jugadoresCnt = 0
        self.estadosCnt = 0
        for fName in fNames:
            rudFile, rudData = self.loadXmltoRUD_DFile(fName)
            if rudData is not None:
                self.jugadoresCnt += rudFile.getStat("numJugadores")
                self.estadosCnt += rudFile.getStat("numEstados")
        t2 = datetime.now()
        t = t2-t1
        print("INFO %s: %s Time processing %d Jugadores %d Estados in RUD_D XML for %s: %s." %
              (func, t2.strftime("%d/%m/%Y %H:%M:%S"), self.jugadoresCnt, self.estadosCnt, mes, t))

    def insertJugadoresRUD_M(self, jugadores, fName):
        func="%s.insertJugadoresRUD_M()" % self.__class__.__name__
        t1 = datetime.now()
        print("DEBUG %s: Insertando jugadores en RUD_M" % func)
        rudm = RUD_M(AppData.db)
        jj = jugadores
        jTot = len(jj)
        doInsertAll=True
        if doInsertAll:
            print("DEBUG %s: Inserto %d jugadores" % (func, len(jj)))
            rudm.insertJugadoresRud(jj, fName)
            rudm.insertEstadosRud(jj, fName)
        else:
            jCnt = 0
            for jugador in jj:
                print("DEBUG %s: Inserto jugador id='%s' (%d/%d)..." % (func, jugador.jugadorId,jCnt,jTot))
                rudm.insertJugadorRud(jugador)
                jCnt += 1
        rudm.conn.commit()
        self.addData(fName, rudm)
        # rudd.conn.close()
        t2 = datetime.now()
        t = t2 - t1
        print("INFO %s: %s: Time inserting %d Jugadores in RUD_M : %s." %
              (func, t2.strftime("%d/%m/%Y %H:%M:%S"), jTot, t))

    def getRUD_MFNames(self, dName = "AJL0005/RU/Mensual/RUD", mes='202302'):
        return self.getFNames(dName, mes)

    def loadXmltoRUD_MFile(self, fName):
        func="%s.loadXMLtoRUD_MFile()" % self.__class__.__name__
        t1 = datetime.now()
        rudFile = self.readXmlRUDFile(self.dMName, fName)
        j = rudFile.jugadores
        print("INFO %s: %d jugadores en '%s'" % (func, len(j), fName))
        rudData = None
        f = (len(j),rudFile.getStat("numEstados"))
        if not self.isFileInControl(f):
            self.addFileToControl(f)
            if self.doInsert:
                rudData = self.insertJugadoresRUD_M(j, fName)
        else:
            errMsg = "Datos duplicados"
            rudFile.addFileError(errMsg)
            print("ERROR %s: %d jugadores en '%s'. %s" % (func, f[0], fName, errMsg))

        t2 = datetime.now()
        t = t2-t1
        print("INFO %s: %s Time processing %d Jugadores in RUD_M XML: %s." %
              (func, t2.strftime("%d/%m/%Y %H:%M:%S"), len(j), t))
        return (rudFile, rudData)

    def loadXmltoRUD_MMes(self, mes="202301"):
        func="%s.loadXMLtoRUD_M()" % self.__class__.__name__
        t1 = datetime.now()

        fNames = self.getRUD_MFNames(self.dMName, mes)
        self.jugadoresCnt = 0
        self.estadosCnt = 0
        #self.doInsert = False
        for fName in fNames:
            #j = self.readXmlRUDFile(self.dMName, fName).jugadores
            #print("INFO %s: %d jugadores en '%s'" % (func, len(j), fName))
            #self.jugadoresCnt += len(j)
            #if self.doInsert:
            #    self.insertJugadoresRUD_M(j)
            rudFile, rudData = self.loadXmltoRUD_MFile(fName)
            if rudData is not None:
                self.jugadoresCnt += rudFile.getStat("numJugadores")
                self.estadosCnt += rudFile.getStat("numEstados")
        t2 = datetime.now()
        t = t2-t1
        print("INFO %s: %s Time processing RUD_M XML. %s %d jugadores, %d estados in  %s." %
              (func, t2.strftime("%d/%m/%Y %H:%M:%S"), mes, self.jugadoresCnt, self.estadosCnt, t))

    def isRUD_DMonthLoaded(self, mes):
        fNames = self.getRUD_DFNames(self.dDName, mes)

        for fName in fNames:
            if not self.contains(fName):
                return False
        return True

    def isRUD_MMonthLoaded(self, mes):
        fNames = self.getRUD_MFNames(self.dMName, mes)

        for fName in fNames:
            if not self.contains(fName):
                return False
        return True


class RUTProcess(FilesProcess):
    def __init__(self, dirDiario="AJL0005/RU/Diario/RUT", dirMensual="AJL0005/RU/Mensual/RUT"):
        """
        Procesa ficheros XML y los inserta en la BBDD Lotba
        :param dirDiario: directorio de los ficheros xml diarios
        :param dirMensual: directorio de los ficheros xml mensuales
        """
        self.doInsert = False
        self.dDName = dirDiario
        self.dMName = dirMensual

    def getRUT_DFNames(self, dName = None, mes='202302'):
        if dName is None:
            dName = self.dDName
        return self.getFNames(dName, mes)


    def isRUT_DMonthLoaded(self, mes):
        fNames = self.getRUT_DFNames(self.dDName, mes)

        for fName in fNames:
            if not self.contains(fName):
                return False
        return True