import json
from datetime import datetime
from mysql import connector
from model.db.mysql.RU.RUD_D import RUD_D
from model.db.mysql.RU.RUD_M import RUD_M

class DBConnectionData():
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

class TestDB():

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

    def testCab(self, dbName):
        host="localhost"
        port="8085"
        database=dbName
        user="tecnalis"
        password= "Stururpqcc45!"

        print("Connecting to %s ..." % dbName)
        data = DBConnectionData(host=host, port=port, database=database, user=user, password=password)
        self.conn = self.connect(data)
        if self.conn is not None:
            print("Connection succesful!")
        else:
            print("ERROR: Connection failed.")

    def showColumns(self, tableName):
        sentence = "SELECT * FROM %s " % tableName
        try:
            cursor = self.conn.cursor()
            cursor.execute(sentence)

            print(" Columns for '%s'" % tableName)
            print([column[0] for column in cursor.description])

        except connector.Error as e:
            print("ERROR: "+e.msg)

    def testInsertRUD_D(self, jugadores):
        t1 = datetime.now()
        print("Insertando jugadores en RUD_M")
        rudd = RUD_M(self.conn)
        jj = jugadores # [:10]
        if True:
            print("Inserto %d jugadores" % len(jj))
            rudd.insertJugadoresRud(jugadores)
        else:
            for jugador in jj:
                print("Inserto jugador id='%s' ..." % jugador.jugadorId)
                rudd.insertJugadorRud(jugador)
        rudd.conn.commit()
        #rudd.conn.close()
        t2 = datetime.now()
        t = t2-t1
        print("%s Time elapsed %s."% (t2.strftime("%d/%m/%Y %H:%M:%S"), t))

    def selectRUD_D(self, tableName="RUD_D"):
        rudd = RUD_D(self.conn)
        rudd.table.name = tableName
        rudd.selectAllRudd()

    def tables_json(self):
        fName = "C:\\Users\\luis.sevilla\\projects\\lotba-xml\\dbmaintain\\lotba3_tables.json"
        data = json.load(open(fName))
        dict = {}
        for d in data:
            for k,v in (d.items()):
                if not k in dict.keys():
                    dict[k] = []
                dict[k].append(v)
        for k in dict.keys():
            print(k)
            for v in dict[k]:
                print("\t%s" % v)
                pass
            print("%s: %d" % (k, len(dict[k])))

'''
Tablas para cargar en LOTBA:
	ACT

	ACT_ApuestasDevolucion_DesgloseOperador
	ACT_Apuestas_DesgloseOperador
	ACT_Comision_DesgloseOperador
	ACT_Otros_DesgloseOperadorConcepto
	ACT_Pozos_DesgloseOperador
	ACT_PremiosEspecie_DesgloseOperador
	ACT_Premios_DesgloseOperador

	CEV

	CJD_Comision_DesgloseOperadorTipoJuego
	CJD_Cuentas

	CJD_D_AjustePremios_DesgloseOperadorTipoJuego
	CJD_D_ApuestasDevolucion_DesgloseOperadorTipoJuego
	CJD_D_Apuestas_DesgloseOperadorTipoJuego
	CJD_D_Depositos_DesgloseMedioPago
	CJD_D_Otros_DesgloseOperadorConcepto
	CJD_D_PremiosEspecie_DesgloseOperadorTipoJuego
	CJD_D_Premios_DesgloseOperadorTipoJuego
	CJD_D_Retiradas_DesgloseMedioPago
	CJD_D_SaldoFinal
	CJD_D_SaldoInicial
	CJD_D_Trans_IN_DesgloseOperador
	CJD_D_Trans_OUT_DesgloseOperador

	CJD_M_AjustePremios_DesgloseOperadorTipoJuego
	CJD_M_ApuestasDevolucion_DesgloseOperadorTipoJuego
	CJD_M_Apuestas_DesgloseOperadorTipoJuego
	CJD_M_Comision_DesgloseOperadorTipoJuego
	CJD_M_Cuentas
	CJD_M_Depositos_DesgloseMedioPago
	CJD_M_Otros_DesgloseOperadorConcepto
	CJD_M_PremiosEspecie_DesgloseOperadorTipoJuego
	CJD_M_Premios_DesgloseOperadorTipoJuego
	CJD_M_Retiradas_DesgloseMedioPago
	CJD_M_SaldoFinal
	CJD_M_SaldoInicial
	CJD_M_Trans_IN_DesgloseOperador
	CJD_M_Trans_OUT_DesgloseOperador

	CJT_D_AjustePremios_DesgloseOperadorTipoJuego
	CJT_D_Bonos_DesgloseOperadorConcepto
	CJT_D_Comision_DesgloseOperadorTipoJuego
	CJT_D_Depositos_DesgloseMedioPago
	CJT_D_Otros_DesgloseOperadorConcepto
	CJT_D_ParticipacionDevolucion_DesgloseOperadorTipoJuego
	CJT_D_Participacion_DesgloseOperadorTipoJuego
	CJT_D_PremiosEspecie_DesgloseOperadorTipoJuego
	CJT_D_Premios_DesgloseOperadorTipoJuego
	CJT_D_Retiradas_DesgloseMedioPago
	CJT_D_SaldoFinal
	CJT_D_SaldoInicial
	CJT_D_Trans_IN_DesgloseOperador
	CJT_D_Trans_OUT_DesgloseOperador

	CJT_M_AjustePremios_DesgloseOperadorTipoJuego
	CJT_M_Bonos_DesgloseOperadorConcepto
	CJT_M_Comision_DesgloseOperadorTipoJuego
	CJT_M_Depositos_DesgloseMedioPago
	CJT_M_Otros_DesgloseOperadorConcepto
	CJT_M_ParticipacionDevolucion_DesgloseOperadorTipoJuego
	CJT_M_Participacion_DesgloseOperadorTipoJuego
	CJT_M_PremiosEspecie_DesgloseOperadorTipoJuego
	CJT_M_Premios_DesgloseOperadorTipoJuego
	CJT_M_Retiradas_DesgloseMedioPago
	CJT_M_SaldoFinal
	CJT_M_SaldoInicial
	CJT_M_Trans_IN_DesgloseOperador
	CJT_M_Trans_OUT_DesgloseOperador

	CPT_PartidasVivas_DesgloseCompromiso
	CPT_PartidasVivas_Movimientos
	CPT_PartidasVivas_SaldoFinal
	CPT_PartidasVivas_SaldoInicial
	CPT_Pozos_DesglosePozo
	CPT_Pozos_Movimientos
	CPT_Pozos_SaldoFinal
	CPT_Pozos_SaldoInicial

	ID

	JUA

	JUD
	JUD_Importe_Apuestas
	JUD_Importe_ApuestasDevolucion
	JUD_Importe_Premios
	JUD_Importe_PremiosEspecie

	JUT_Apuestas
	JUT_Apuestas_DesgloseCruzadas
	JUT_Apuestas_DesgloseCruzadas_Cruces
	JUT_Apuestas_Eventos
	JUT_BlackJack
	JUT_PokerCash
	JUT_PokerTorneo
	JUT_PuntoBanca
	JUT_Ruleta
	JUT_Totales_Participacion
	JUT_Totales_ParticipacionDevolucion
	JUT_Totales_Pozos
	JUT_Totales_Premios
	JUT_Totales_PremiosEspecie
	JUT_Tragamonedas

	RUD_D
	RUD_D_Estado
	RUD_M
	RUD_M_Estado
	
	RUT_D
	RUT_D_NumeroApostadoresPorEstado
	RUT_M
	RUT_M_NumeroApostadoresPorEstado

	process_log
	process_log_mrj
'''