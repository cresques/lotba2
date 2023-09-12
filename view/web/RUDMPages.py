from flask import Flask
from view.web.WebPage import WebPage
from controler.AppData import AppData
from controler.RU.RUProcess import RUDProcess

app = Flask(__name__)

class RUMPages(WebPage):
    title = "LOTBA: Carga historicos"
    rootLabel = "Carga históricos LOTBA"
    parentPage, parentLabel = "/RUD_D", "Cargar RUD_D"
    def show_RUD_M(self):
        """
        Pagina /RUD_M
        :return: pagina completa
        """
        end = "\t</body>\n</html>\n"
        mes = "202212"
        body = '<a href="/">%s</a> - %s\n<br>\n<br>\n' % (self.rootLabel, self.parentLabel)
        body += self.bodyRUD_MTodos()
        return self.head(self.title)+body+end

    def bodyRUD_MTodos(self):
        proc = RUDProcess()
        meses = proc.getMeses()
        body = "\t<ul>\n"
        fCnt = 0
        for mes in meses:
            fNames = proc.getRUD_MFNames(mes=mes)
            body += '<li><a href="/RUD_M_Mes/%s/Ver">%s (%2d files)</a>\n' % (mes, mes, len(fNames))
            fCnt += len(fNames)
        body += "\t</ul>"
        body = ("%d ficheros para cargar. \r\n" % fCnt) + body
        return body

    def show_RUD_M_Mes(self, mes, cargar="Ver"):
        """
        Pagina /RUD_M_Mes/<mes>/<cargar>
        Permite importar todo el mes de una vez. Si ya esta cargado solo se visualiza
        :param mes: El mes a ver/Cargar
        :param cargar: Ver o Carga
        :return: pagina completa
        """
        end = "\t</body>\n</html>\n"
        #mes = "202212"
        body = '<a href="/">Carga históricos LOTBA</a> - ' + \
               '<a href="/RUD_M">Cargar RUD_M</a> - ' + \
                mes + \
               '\n<br>\n<br>\n'
        body += self.bodyRUD_M(mes, cargar)
        return self.head("LOTBA: Carga historicos")+body+end

    def bodyRUD_M(self, mes="202301", cargar="Ver"):
        proc = RUDProcess()
        fNames = proc.getRUD_MFNames(mes=mes)

        if (cargar == "Carga"):
            # Aqui llamo a cargar todo el mes
            AppData.getAppStart().loadRUD_M(mes)
            pass
        monthLoaded = proc.isRUD_MMonthLoaded(mes)
        if (cargar != "Carga" and not monthLoaded):
            body = "<b>%s</b>: %d ficheros para cargar. \r\n" % (mes, len(fNames))
            body += self.buttonRUD_MLoadMonth(mes=mes)
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
                errMsg = 'Error insertando' if len(status['errors']) > 0 else ''
                cntJugadores += nj
                cntEstados += ne
                body += '\t\t<tr><td><a href="/RUD_M_LoadXml/%s/%s"></a>%s</td>' % (mes,fName,fName)
                body += '<td align="right">%s</td>' % "{0:n}".format(nj)
                body += '<td align="right">%s</td>\r\n' % "{0:n}".format(ne)
                body += '<td class="error">%s</td>\r\n' % errMsg
                body += '\t\t</tr>\r\n'
            else:
                body += '\t\t<tr><td><a href="/RUD_M_LoadXml/%s/%s">%s</a></td>' % (mes, fName, fName)
                body += '<td colspan="3"></td>\r\n'
                body += '\t\t</tr>\r\n'
        body += '\t\t<tr><td>&nbsp;&nbsp;&nbsp;Total</td>'
        body += '<td align="right">%s</td>' % "{0:n}".format(cntJugadores)
        body += '<td align="right">%s</td></tr>\r\n' % "{0:n}".format(cntEstados)
        body += "\t</table>\r\n"
        return body

    def buttonRUD_MLoadMonth(self, mes):
        ret = '&nbsp;&nbsp;&nbsp;<a href=/RUD_M_Mes/%s/Carga><button class=txt style="height:22px;width:80px"\r\n\t\t><b>Cargar mes</b></button></a>' % mes
        return ret

    def show_RUD_M_LoadXml(self, mes, fName):
        """
        Permite importar Un fichero XML. Si ya esta cargado solo se visualiza
        :param mes: El mes
        :param fName: el Nombre del fichero
        :return: pagina completa
        """
        end = "\t</body>\n</html>\n"
        body = '<a href="/">Carga históricos LOTBA</a> - ' + \
               '<a href="/RUD_M">Cargar RUD_M</a> - ' + \
               '<a href="/RUD_M_Mes/%s/Ver">%s</a> - ' % (mes, mes) + \
               fName + \
               '\n<br>\n<br>\n'
        body += self.bodyRUD_M_LoadXml(mes, fName)
        return self.head("LOTBA: Carga historicos") + body + end

    def bodyRUD_M_LoadXml(self, mes, fName):
        body = "\t<table>\n\t<tr>"
        proc = RUDProcess()
        proc.doInsert = True
        proc.loadXmltoRUD_MFile(fName)
        status = proc.getStats(fName)
        body += "\t\t<td>Jugadores</td><td>%d</td>\n" % status['numJugadores']
        body += "\t</tr><tr>\n"
        body += "\t\t<td>Estados</td><td>%d</td>\n" % status['numEstados']
        for msg in status['errors']:
            body += '</tr>\n\t\t<tr><td colspan="2" class="error">%s</td>\n' % msg
        body += "\t</tr>\n\t</table>\n"
        return body