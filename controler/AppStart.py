import os, locale
from datetime import datetime
from controler.AppData import AppData
from controler.RU.RUProcess import RUDProcess
from view.web.start import app

class Msger():
    """
    Message list
    """
    msg = []

    def __init__(self):
        self.clear()

    def clear(self):
        """
        Clears all messages
        :return:
        """
        self.msg = []

    def add(self, msg):
        """
        Adds new message
        :param msg:
        :return:
        """
        self.msg.append(msg)

    def print(self):
        """
        Sends all messages to console
        :return:
        """
        for msg in self.msg:
            print(msg)

class AppStart():
    dataDir = "/LOTBA"

    def __init__(self):
        func = "%s.__init__()" % self.__class__.__name__

    def appInit(self):
        func = "%s.appInit()" % self.__class__.__name__
        self.t1 = datetime.now()
        locale.setlocale(locale.LC_ALL, 'es_ES')
        dbName = "LOTBA3"
        print("INFO %s: %s LOTBA file load starting in %s..." % (func,
            self.t1.strftime("%d/%m/%Y %H:%M:%S"), dbName))
        AppData("C:\\Users\\luis.sevilla\\projects\\lotba-xml\\LOTBA", dbName, self)

    def appFinish(self):
        func = "%s.appFinish()" % self.__class__.__name__
        print("INFO %s: LOTBA: ending in %s..." % (func, AppData.db.dbName))

    def showColumns(self, tName="RUD_M"):
        AppData.db.showColumns(tName)

    def showDBErrors(self):
        func = "%s.showDBErrors()" % self.__class__.__name__
        appMsg = Msger()
        # mes = "202301"
        appMsg.clear()
        appMsg.add("\nINFO %s:   DB Errors: " % func)
        for msg in AppData.db.getDbErrors():
            appMsg.add(msg)
        appMsg.print()

    def showRUTColumns(self):
        for table in ("RUT_D", "RUT_D_NumeroApostadoresPorEstado", "RUT_M", "RUT_M_NumeroApostadoresPorEstado"):
            self.showColumns(table)

    def loadRUD_D(self, mes):
        func = "%s.loadRUD_D()" % self.__class__.__name__
        t1 = datetime.now()
        proc = RUDProcess()
        proc.doInsert = True
        proc.loadXmltoRUD_DMes(mes)
        t2 = datetime.now()
        t = t2 - t1
        self.appMsg.add("INFO %s: %s Time processing %7s Jugadores in RUD_D XML for %s: %s." %
                        (func, t2.strftime("%d/%m/%Y %H:%M:%S"), f"{proc.jugadoresCnt:n}", mes, t))

    def loadRUD_M(self, mes):
        func = "%s.loadRUD_M()" % self.__class__.__name__
        t1 = datetime.now()
        proc = RUDProcess()
        proc.doInsert = True
        proc.loadXmltoRUD_MMes(mes)
        t2 = datetime.now()
        t = t2 - t1
        self.appMsg.add("INFO %s: %s Time processing %7s Jugadores in RUD_M XML for %s: %s." %
              (func, t2.strftime("%d/%m/%Y %H:%M:%S"), f"{proc.jugadoresCnt:n}", mes, t))

    def start(self):
        """
        Starts aplication.

        :return:
        """
        func="%s.start()" % self.__class__.__name__

        self.appInit()
        self.appMsg = appMsg = Msger()
        mes = "202301"
        appMsg.clear()
        appMsg.add("\nINFO %s:   Summary: " % func)
        # app.showColumns("RUD_M")
        self.loadRUD_D(mes)
        # app.testLoadRUD_M("202301")
        # app.printMsg()
        # app.showDBErrors()
        #self.showRUTColumns()
        self.appFinish()

        self.t2 = datetime.now()
        t = self.t2 - self.t1
        print("INFO %s: %s Total running time: %s." %
              (func, self.t2.strftime("%d/%m/%Y %H:%M:%S"), t))

    def webStart(self):
        func="%s.start()" % self.__class__.__name__

        self.appInit()
        self.appMsg = appMsg = Msger()
        #app.setAppStart(self)
        app.run()
        self.appFinish()
