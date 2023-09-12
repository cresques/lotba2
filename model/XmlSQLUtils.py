class XSUtils():
    @staticmethod
    def fmtDateTimeToSQL( d ):
        """
        Formatea una fecha y hora para Insertar en SQL
        Si d es None devuelve None
        :param d:
        :return:
        """
        if d is None:
            return None
        return "%s-%s-%s %s:%s:%s" % ( d[0:+4], d[4:6], d[6:8], d[8:10], d[10:12], d[12:14] )

    @staticmethod
    def fmtDateToSQL( d ):
        if d is None:
            return None
        return "%s-%s-%s" % ( d[0:+4], d[4:6], d[6:8] )