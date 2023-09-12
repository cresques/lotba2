from xml.dom import minidom
import xml.etree.ElementTree as et
from model.xml.XmlFile import XmlFile
from model.data.RU.RUJugador import RUJugador

class RUD(XmlFile):
    """
    Lee los ficheros XML de RUD: RUD_D* y RUD_M*
    """
    jugadores = []
    def __init__(self, fName):
        self.debug = False
        XmlFile.__init__(self, fName)
        self.jugadores = []
        self.judadoresDefecto = []

    def parseFile(self):
        doc = minidom.parse(self.fName)
        if (self.debug):
            print(doc.nodeName)
            print(doc.firstChild.tagName)
        eTot = 0
        for reg in doc.getElementsByTagName("Registro"):
            jCnt, eCnt = self.parseReg(reg)
            eTot += eCnt
        self.setStat("numJugadores", len(self.jugadores))
        self.setStat("numEstados", eTot)

    def parseReg(self, reg):
        func="%s.parseReg()" % self.__class__.__name__
        # En caso de RUD_D
        dia = self.getDataByTagName(reg, "Dia")
        if dia != None and self.debug:
            print("DEBUG %s: Dia %s" % (func, dia))
        # En caso de RUD_M
        mes = self.getDataByTagName(reg, "Mes")
        if mes != None and self.debug:
            print("DEBUG %s: Mes %s" % (func, mes))
        jugadores = reg.getElementsByTagName("Jugador")
        estados = 0
        for jugador in jugadores:
            j = self.parseJugador(jugador)
            j.dia = dia
            j.mes = mes
            if not j.defecto:
                self.jugadores.append(j)
                estados += len(j.historico)
            else:
                print("\t jugador %s defectuoso" % j.jugadorId)
                self.judadoresDefecto.append(j)
        if self.debug:
            print("DEBUG %s: Jugadores: %d " % (func, len(jugadores)))
        return (len(jugadores), estados)


    def parseJugador(self, jugador):
        func="%s.parseJugador()" % self.__class__.__name__
        j = RUJugador()
        j.defecto = False
        # ID
        j.operadorId = jugador.getElementsByTagName("OperadorId")[0].firstChild.data
        j.jugadorId = jugador.getElementsByTagName("JugadorId")[0].firstChild.data
        if self.debug:
            print("DEBUG %s: Jugador %s" % (func, j.jugadorId))
        j.fechaActivacion = jugador.getElementsByTagName("FechaActivacion")[0].firstChild.data
        j.cambiosEnDatos = jugador.getElementsByTagName("CambiosEnDatos")[0].firstChild.data
        # Residente
        j.nacionalidad = jugador.getElementsByTagName("Nacionalidad")[0].firstChild.data
        j.dni = self.getDataByTagName(jugador, "DNI")
        if j.dni is None: j.defecto = True
        # No residente
        j.NoResidente_Nacionalidad = None
        j.NoResidente_Documento = None
        j.NoResidente_PaisResidencia = None
        j.NoResidente_TipoDocumento = None
        j.NoResidente_EspecificarTipoDocumento = None
        j.fechaNacimiento = self.getDataByTagName(jugador, "FechaNacimiento")
        if j.fechaNacimiento is None: j.defecto = True
        j.login = self.getDataByTagName(jugador, "Login")
        # CUIT
        j.documento = self.getDataByTagName(jugador, "Documento")

        j.nombre = jugador.getElementsByTagName("Nombre")[0].firstChild.data
        j.apellido = jugador.getElementsByTagName("Apellido")[0].firstChild.data
        j.email = jugador.getElementsByTagName("email")[0].firstChild.data
        j.sexo = jugador.getElementsByTagName("Sexo")[0].firstChild.data
        j.estadoCivil = self.getDataByTagName(jugador, "EstadoCivil")
        # Domicilio
        j.direccion = self.getDataByTagName(jugador, "Direccion")
        j.ciudad = self.getDataByTagName(jugador, "Ciudad")
        j.pais = jugador.getElementsByTagName("Pais")[0].firstChild.data

        j.telefono = self.getDataByTagName(jugador, "Telefono")
        j.ocupacion = self.getDataByTagName(jugador, "Ocupacion")
        j.pep = jugador.getElementsByTagName("PEP")[0].firstChild.data
        j.rePET = jugador.getElementsByTagName("RePET")[0].firstChild.data
        # LimitesDeposito
        j.limiteDiario = jugador.getElementsByTagName("Diario")[0].firstChild.data
        j.limiteSemanal = jugador.getElementsByTagName("Semanal")[0].firstChild.data
        j.limiteMensual = jugador.getElementsByTagName("Mensual")[0].firstChild.data

        j.limitesGasto = jugador.getElementsByTagName("LimitesGasto")[0].firstChild.data
        j.limitesTiempo = jugador.getElementsByTagName("LimitesTiempo")[0].firstChild.data
        j.limitesPerdida = jugador.getElementsByTagName("LimitesPerdida")[0].firstChild.data
        # Estado
        self.parseEstado(jugador, j)
        if self.debug:
            print("DEBUG %s: Jugador %s: %d estados" % (func, j.jugadorId, len(j.historico)))

        j.vDocumental = jugador.getElementsByTagName("VDocumental")[0].firstChild.data
        j.fVDocumental = self.getDataByTagName(jugador, "FVDocumental")

        if self.debug:
            print("%4d %7s %s" % (len(self.jugadores), j.jugadorId, j.fechaNacimiento))
        return j

    def parseEstado(self, jugador, j):
        j.estado = self.getDataByTagName(jugador, "Estado")
        j.estadoOperador = self.getDataByTagName(jugador, "EstadoOperador")
        j.desde = self.getDataByTagName(jugador, "Desde")
        j.historico = []
        for historico in jugador.getElementsByTagName("Historico"):
            j.historico.append(self.parseHistorico(historico))

    def parseHistorico(self, historico):
        h = {}
        h['EstadoCNJ'] = historico.getElementsByTagName("EstadoCNJ")[0].firstChild.data
        h['EstadoOperador'] = historico.getElementsByTagName("EstadoOperador")[0].firstChild.data
        h['Desde'] = historico.getElementsByTagName("Desde")[0].firstChild.data
        return h

    def _testEtree(self, etree):
        pass

    def parse2(self):
        etree = et.parse(self.fName)
        self._testEtree(etree)