class SQLUtils():
    @staticmethod
    def toSqlStr(str):
        """ Devuelve NULL o 'str' a partir del argumento

        :param str: Cadena a procesar
        :return: Resultado
        """
        if str == None:
            return "NULL"
        return "'%s'" % str