from flask import Flask
from view.web.WebPage import WebPage
from controler.AppData import AppData
from controler.RU.RUProcess import RUTProcess

app = Flask(__name__)

class RUTDPages(WebPage):
    title = "LOTBA: Carga historicos"
    rootLabel = "Carga históricos LOTBA"
    parentPage, parentLabel = "/RUT_D", "Cargar RUT_D"
    def show_RUT_D(self):
        """
        Pagina /RUT_D
        :return: pagina completa
        """
        end = "\t</body>\n</html>\n"
        mes = "202212"
        body = '<a href="/">%s</a> - %s\n<br>\n<br>\n' % (self.rootLabel, self.parentLabel)
        body += self.bodyRUT_DTodos()
        return self.head(self.title)+body+end

    def bodyRUT_DTodos(self):
        proc = RUTProcess()
        meses = proc.getMeses()
        body = "\t<ul>\n"
        fCnt = 0
        for mes in meses:
            fNames = proc.getRUT_DFNames(mes=mes)
            body += '<li><a href="/RUT_D_Mes/%s/Ver">%s (%2d files)</a>\n' % (mes, mes, len(fNames))
            fCnt += len(fNames)
        body += "\t</ul>"
        body = ("%d ficheros para cargar. \r\n" % fCnt) + body
        return body

    def show_RUT_D_Mes(self, mes, cargar="Ver"):
        """
        Pagina /RUT_D_Mes/<mes>/<cargar>
        Permite importar todo el mes de una vez. Si ya esta cargado solo se visualiza
        Pagina /RUT_D_LoadXml/<mes>/<fName>
        :return: pagina completa
        """
        end = "\t</body>\n</html>\n"
        #mes = "202212"
        body = '<a href="/">Carga históricos LOTBA</a> - ' + \
               '<a href="%s">%s</a> - ' % (self.parentPage, self.parentLabel) + \
               mes + \
               '\n<br>\n<br>\n'
        body += self.bodyRUT_D(mes, cargar)
        return self.head(self.title)+body+end

    def bodyRUT_D(self, mes="202301", cargar="Ver"):
        proc = RUTProcess()
        fNames = proc.getRUT_DFNames(mes=mes)

        if (cargar == "Carga"):
            # Aqui llamo a cargar todo el mes
            AppData.getAppStart().loadRUD_D(mes)
            pass
        monthLoaded = proc.isRUT_DMonthLoaded(mes)
        if (cargar != "Carga" and not monthLoaded):
            body = "<b>%s</b>: %d ficheros para cargar. \r\n" % (mes, len(fNames))
            body += self.buttonRUT_DLoadMonth(mes=mes)
        else:
            body = "<b>%s</b>: %d ficheros cargados. \r\n" % (mes, len(fNames))
        body += "\t<table>\r\n"
        body += '\t\t<tr><th>Fichero</th><th align="right">Jugadores</th><th align="right">Estados</th></tr>'
        cntEstados = cntJugadores = 0
        for fName in fNames:
            if (proc.contains(fName)):
                status = proc.getStats(fName)
                nj = status['numJugadores']
                ne = status['numEstados']
                errMsg = status['errors'][0] if len(status['errors']) > 0 else ''
                cntJugadores += nj
                cntEstados += ne
                body += '\t\t<tr><td><a href="/RUD_D_LoadXml/%s/%s"></a>%s</td>' % (mes,fName,fName)
                body += '<td align="right">%s</td>' % "{0:n}".format(nj)
                body += '<td align="right">%s</td>\r\n' % "{0:n}".format(ne)
                body += '<td class="error">%s</td>\r\n' % errMsg
                body += '\t\t</tr>\r\n'
            else:
                body += '\t\t<tr><td><a href="/RUD_D_LoadXml/%s/%s">%s</a></td>' % (mes, fName, fName)
                body += '<td colspan="3"></td>\r\n'
                body += '\t\t</tr>\r\n'
        body += '\t\t<tr><td>&nbsp;&nbsp;&nbsp;Total</td>'
        body += '<td align="right">%s</td>' % "{0:n}".format(cntJugadores)
        body += '<td align="right">%s</td></tr>\r\n' % "{0:n}".format(cntEstados)
        body += "\t</table>\r\n"
        return body

    def buttonRUT_DLoadMonth(self, mes):
        ret = '&nbsp;&nbsp;&nbsp;<a href=/RUD_D_Mes/%s/Carga><button class=txt style="height:22px;width:80px"\r\n\t\t><b>Cargar mes</b></button></a>' % mes
        return ret

    def show_RUD_D_LoadXml(self, mes, fName):
        return ""
