from controler.FilesProcess import FilesProcess


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


    def getRUD_DFNames(self, dName = "AJL0005/JU/", mes='202302'):
        return self.getFNames(dName, mes)

