from mysql import connector

class DBConnectionData():
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = self.dbName = database
        self.user = user
        self.password = password

class DB():
    def __init__(self):
        self.__dbErrors = []

    def connect(self, data):
        conn = None
        try:
            conn = connector.connect( host=data.host, port=data.port,
                database=data.database, user=data.user, password=data.password)
            if conn.is_connected():
                return conn
        except connector.Error as e:
            print(e)
        #finally:
        #    if conn is not None and conn.is_connected():
        #        conn.close()
        return None

    def openCabSlave2DB(self, dbName):
        func="%s.openCabSlave2DB()" % self.__class__.__name__
        self.dbName = dbName
        slave2tunnel = ("localhost",8085,"tecnalis","Stururpqcc45!")
        slave2 = ("192.16.94.140",3306,"tecnalis","Stururpqcc45!") # No va
        host,port,user,password = slave2tunnel

        print("INFO %s: Connecting to %s ..." % (func, dbName))
        data = DBConnectionData(host=host, port=port, database=dbName, user=user, password=password)

        self.conn = self.connect(data)
        if self.conn is not None:
            print("INFO %s: Connection succesful!" % func)
        else:
            print("ERROR %s: Connection failed." % func)
        return self.conn

    def close(self):
        self.conn.close()

    def showColumns(self, tableName):
        func="%s.showColumns()" % self.__class__.__name__
        sentence = "SELECT * FROM %s " % tableName
        try:
            # Anyado Buffered para evitar mysql.connector.errors.InternalError: Unread result found
            cursor = self.conn.cursor(buffered=True)
            cursor.execute(sentence)

            print("INFO %s: Columns for '%s' = %d" % (func, tableName, len(cursor.description)))
            msg = "["
            str = ""
            for col in cursor.description:
                str += "'%s', " % col[0]
                if (len(str)>= 100):
                    msg += str + '\n'
                    str = ''
            msg += str + ']'
            print("INFO %s: %s" % (func, msg))
            #print([column[0] for column in cursor.description])
        except connector.Error as e:
            print("ERROR %s: " % (func, e.msg))
        finally:
            cursor.close()

    def dbError(self, msg):
        """
        adds a database Error
        :param msg:
        :return:
        """
        self.__dbErrors.append(msg)

    def getDbErrors(self):
        return self.__dbErrors