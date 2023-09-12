from model.db.mysql.DB import DB

class AppData():
    dataDir = None
    db = None
    __appStart = None

    def __init__(self, dataDir, dbName, appStart):
        AppData.dataDir = dataDir
        AppData.startCabSlave2(dbName)
        AppData.__appStart = appStart

    @staticmethod
    def startCabSlave2(dbName):
        AppData.db = DB()
        AppData.db.openCabSlave2DB(dbName)

    @staticmethod
    def getAppStart():
        return AppData.__appStart


    @staticmethod
    def icConnected():
        return AppData.db.conn is not None