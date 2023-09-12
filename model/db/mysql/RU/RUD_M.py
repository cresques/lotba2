from model.XmlSQLUtils import XSUtils
from model.db.mysql.RU.RUD_D import RUD_D

class RUD_M(RUD_D):
    def __init__(self, connector):
        RUD_D.__init__(self, connector)
        self.tableRud.name = "RUD_M"

        self.tableRudEstado.name = "RUD_M_Estado"
        self.tableRudEstado.columns = ['Anno', 'Mes', 'JugadorId', 'Desde', 'EstadoCNJ', 'EstadoOperador']

        self.initInsertRud()
        self.initInsertEstadoRud()

    def initInsertRud(self):
        rudInsertColumns = """`Anno`, `Mes`, `JugadorId`, `FechaActivacion`, `CambioDatos`, `Residente_Nacionalidad`,
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
             %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    def initInsertEstadoRud(self):
        rudInsertEstadoColumns = """`Anno`, `Mes`, `JugadorId`, `Desde`, `EstadoCNJ`, `EstadoOperador`"""
        self.rudInsertEstadoMask = "INSERT INTO " + self.tableRudEstado.name + "(" + rudInsertEstadoColumns + """) VALUES(
             %s,%s,%s,%s,%s,%s)"""

    def toValues(self, jugador):
        j = jugador
        return (
            j.mes[0:4],
            j.mes[4:6],
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
                j.mes[0:4],
                j.mes[4:6],
                j.jugadorId,
                XSUtils.fmtDateTimeToSQL(h['Desde']),
                h['EstadoCNJ'],
                h['EstadoOperador']
            ))
        return v

