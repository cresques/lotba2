from mysql import connector
from model.Storage import Stats
from model.db.SQLUtils import SQLUtils
from model.db.Table import Table
from model.XmlSQLUtils import XSUtils

class RUD_D(Stats):
    def __init__(self, db):
        Stats.__init__(self)
        self.db = db
        self.conn = db.conn
        self.tableRud = Table()
        self.tableRud.name = "RUD_D"
        self.tableRud.columns = ['Dia', 'JugadorId', 'FechaActivacion', 'CambioDatos',
            'Residente_Nacionalidad', 'Residente_DNI','NoResidente_Nacionalidad', 'NoResidente_Documento',
            'NoResidente_PaisResidencia', 'NoResidente_TipoDocumento', 'NoResidente_EspecificarTipoDocumento',
            'FechaNacimiento', 'Login', 'Pseudonimo', 'CUIT', 'Nombre', 'Apellido', 'email', 'Sexo',
            'EstadoCivil', 'Domicilio_Direccion', 'Domicilio_Ciudad', 'Domicilio_Pais', 'Telefono',
            'Ocupacion', 'PEP', 'RePET', 'LimitesDepositoDiario', 'LimitesDepositoSemanal',
            'LimitesDepositoMensual', 'LimitesGasto', 'LimitesTiempo', 'LimitesPerdida',
            'VDocumental', 'FVDocumental']

        self.tableRudEstado = Table()
        self.tableRudEstado.name = "RUD_D_Estado"
        self.tableRudEstado.columns = ['Dia', 'JugadorId', 'Desde', 'EstadoCNJ', 'EstadoOperador']

        self.initInsertRud()
        self.initInsertEstadoRud()

    '''
    Export de la LOTBA.RUD_D
        insert into `RUD_D` (`Dia`, `JugadorId`, `FechaActivacion`, `CambioDatos`, `Residente_Nacionalidad`,
            `Residente_DNI`, `NoResidente_Nacionalidad`, `NoResidente_Documento`, `NoResidente_PaisResidencia`,
            `NoResidente_TipoDocumento`, `NoResidente_EspecificarTipoDocumento`, `FechaNacimiento`, `Login`,
            `Pseudonimo`, `CUIT`, `Nombre`, `Apellido`, `email`, 
            `Sexo`, `EstadoCivil`, `Domicilio_Direccion`, `Domicilio_Ciudad`, `Domicilio_Pais`, `Telefono`, 
            `Ocupacion`, `PEP`, `RePET`, 
            `LimitesDepositoDiario`, `LimitesDepositoSemanal`, `LimitesDepositoMensual`, `LimitesGasto`, 
            `LimitesTiempo`, `LimitesPerdida`, `VDocumental`, `FVDocumental`)
        values('2022-09-05','1697','2021-07-10 02:06:38','S','AR',
            '40228300', NULL, NULL, NULL, 
            NULL, NULL,'1997-02-11','francodc97',
            'francodc97','23402283009','Franco Daniel','De Caria','francoddc1997@gmail.com',
            'M','Soltero','CASTRO BARROS | 1918 | DTO 2 |','CABA','AR', '54-011-21648045',
            'Estudiante','No','No',
            '15000.00','50000.00','85500.00','1500000.00',
            '6.00', '1500000.00','S','2021-07-10 02:06:38');
    '''
    def initInsertRud(self):
        rudInsertColumns = """`Dia`, `JugadorId`, `FechaActivacion`, `CambioDatos`, `Residente_Nacionalidad`,
            `Residente_DNI`,
            `NoResidente_Nacionalidad`, `NoResidente_Documento`, `NoResidente_PaisResidencia`,
            `NoResidente_TipoDocumento`, `NoResidente_EspecificarTipoDocumento`, `FechaNacimiento`, `Login`,
            `Pseudonimo`, `CUIT`, `Nombre`, `Apellido`, `email`,
            `Sexo`, `EstadoCivil`, `Domicilio_Direccion`, `Domicilio_Ciudad`, `Domicilio_Pais`, `Telefono`,
            `Ocupacion`, `PEP`, `RePET`,
            `LimitesDepositoDiario`, `LimitesDepositoSemanal`, `LimitesDepositoMensual`, `LimitesGasto`,
            `LimitesTiempo`, `LimitesPerdida`, `VDocumental`, `FVDocumental`"""
        self.rudInsertmask = "INSERT INTO " + self.tableRud.name + "(" + rudInsertColumns + """) VALUES(
             %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
             %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    def initInsertEstadoRud(self):
        rudInsertEstadoColumns = """`Dia`, `JugadorId`, `Desde`, `EstadoCNJ`, `EstadoOperador`"""
        self.rudInsertEstadoMask = "INSERT INTO " + self.tableRudEstado.name + "(" + rudInsertEstadoColumns + """) VALUES(
             %s,%s,%s,%s,%s)"""

    def toValues(self, jugador):
        j = jugador
        return (
            XSUtils.fmtDateToSQL(j.dia),
            j.jugadorId,
            XSUtils.fmtDateTimeToSQL(j.fechaActivacion),
            j.cambiosEnDatos,
            j.nacionalidad,
            j.dni,
            j.NoResidente_Nacionalidad,
            j.NoResidente_Documento,
            j.NoResidente_PaisResidencia,
            j.NoResidente_TipoDocumento,
            j.NoResidente_EspecificarTipoDocumento,
            XSUtils.fmtDateToSQL(j.fechaNacimiento),
            j.login,
            j.login,
            j.documento,
            j.nombre,
            j.apellido,
            j.email,
            j.sexo,
            j.estadoCivil,
            j.direccion,
            j.ciudad,
            j.pais,
            j.telefono,
            j.ocupacion,
            j.pep,
            j.rePET,
            j.limiteDiario,
            j.limiteSemanal,
            j.limiteMensual,
            j.limitesGasto,
            j.limitesTiempo,
            j.limitesPerdida,
            j.vDocumental,
            XSUtils.fmtDateTimeToSQL(j.fVDocumental)
        )

    def estadoToValues(self, jugador):
        j = jugador
        v = []
        for h in j.historico:
            v.append((
                XSUtils.fmtDateToSQL(j.dia),
                j.jugadorId,
                XSUtils.fmtDateTimeToSQL(h['Desde']),
                h['EstadoCNJ'],
                h['EstadoOperador']
            ))
        return v

    def toSQLvalues(self, values):
        ret = []
        for v in values:
            ret.append(SQLUtils.toSqlStr(v))
        return tuple(ret)

    def insertJugadorRud(self, jugador):
        j = jugador
        #dia = XSUtils.fmtDateToSQL(j.dia)
        #print("%s %s" % (dia, j.jugadorId))

        values = self.toValues(j)

        sentence = self.rudInsertmask % self.toSQLvalues(values)

        #print(sentence)
        try:
            cursor = self.conn.cursor()
            cursor.execute(sentence)

            self.conn.commit()
        except connector.Error as e:
            msg = "ERROR: "+e.msg
            print(msg)
            self.db.dbError(msg)
        finally:
            cursor.close()

    def insertJugadoresRud(self, jugadores, fName):
        func="%s.insertJugadoresRud()" % self.__class__.__name__
        #dia = XSUtils.fmtDateToSQL(j.dia)
        #print("%s %s" % (dia, j.jugadorId))
        self.setStat('XmlFile', fName)
        values = []
        for j in jugadores:
            values += [self.toValues(j)]
        print("DEBUG %s: %s" % (func, values[0][0]))
        sentence = self.rudInsertmask

        print("INFO %s: Inserting %d jugadores" % (func, len(jugadores)))
        try:
            cursor = self.conn.cursor()
            cursor.executemany(sentence, values)

            self.conn.commit()
        except connector.Error as e:
            msg = "ERROR %s: %s" % (func, e.msg)
            print(msg)
            self.db.dbError(msg)
            self.addError(msg)
        finally:
            cursor.close()

    def insertEstadosRud(self, jugadores, fName):
        func="%s.insertEstadosRud()" % self.__class__.__name__
        #dia = XSUtils.fmtDateToSQL(j.dia)
        #print("%s %s" % (dia, j.jugadorId))

        values = []
        for j in jugadores:
            values += self.estadoToValues(j)
        print("DEBUG %s: %s" % (func, values[0][0]))
        sentence = self.rudInsertEstadoMask

        print("INFO %s: Inserting %d jugadores, %d estados" % (func, len(jugadores), len(values)))
        try:
            cursor = self.conn.cursor()
            cursor.executemany(sentence, values)

            self.conn.commit()
        except connector.Error as e:
            msg = "ERROR %s: %s" % (func, e.msg)
            print(msg)
            self.db.dbError(msg)
            self.addError(msg)
        finally:
            cursor.close()

    def selectAllRud(self):
        func="%s.selectAllRud()" % self.__class__.__name__
        sentence = "SELECT * FROM %s" % self.tableRud.name

        try:
            cursor = self.conn.cursor()
            cursor.execute(sentence)

            rows = cursor.fetchall()
            print("INFO %s: Total Row(s) %d " % (func, cursor.rowcount))

        except connector.Error as e:
            print("ERROR %s: %s" % (func, e.msg))