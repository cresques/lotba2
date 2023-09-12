from xml.dom import minidom
import xml.etree.ElementTree as et
from model.xml.XmlFile import XmlFile
from model.data.RU.RUJugador import RUJugador

class RUT(XmlFile):
    """
    Lee los ficheros XML de RUT para cargar en:
        "RUT_D"
        "RUT_D_NumeroApostadoresPorEstado"
        "RUT_M"
        "RUT_M_NumeroApostadoresPorEstado"
    """

    apostadores = []
    debug = True
    def __init__(self, fName):
        #super.__init__(self, fName)
        self.fName = fName
        self.apostadores = []

    def parseFile(self):
        doc = minidom.parse(self.fName)
        if (self.debug):
            print(doc.nodeName)
            print(doc.firstChild.tagName)
        for reg in doc.getElementsByTagName("Registro"):
            self.parseReg(reg)

    def parseReg(self, reg):
        func="%s.parseReg()" % self.__class__.__name__
        # En caso de RUT_D
        fecha = self.getDataByTagName(reg, "Fecha")
        if fecha != None:
            print("DEBUG %s: Fecha %s" % (func, fecha))
        dia = self.getDataByTagName(reg, "Dia")
        if dia != None:
            print("DEBUG %s: Dia %s" % (func, dia))
        # En caso de RUT_M
        mes = self.getDataByTagName(reg, "Mes")
        if mes != None:
            print("DEBUG %s: Mes %s" % (func, mes))
        apostadoresPorEstado = reg.getElementsByTagName("NumeroApostadoresPorEstado")
        for porEstado in apostadoresPorEstado:
            j = self.parseJugador(jugador)
            j.dia = dia
            j.mes = mes
            self.jugadores.append(j)
        if (self.debug):
            print("DEBUG %s: Jugadores: %d " % (func, len(jugadores)))

    def parseJugador(self, jugador):
        func="%s.parseJugador()" % self.__class__.__name__
        j = RUJugador()
        # ID
        j.operadorId = jugador.getElementsByTagName("OperadorId")[0].firstChild.data
        j.jugadorId = jugador.getElementsByTagName("JugadorId")[0].firstChild.data
        if self.debug:
            print("DEBUG %s: Jugador %s" % (func, j.jugadorId))
        j.fechaActivacion = jugador.getElementsByTagName("FechaActivacion")[0].firstChild.data
