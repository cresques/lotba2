from flask import Flask
from controler.AppData import AppData
from view.web.WebPage import WebPage
from view.web.RUDDPages import RUDPages
from view.web.RUDMPages import RUMPages
from view.web.RUTDPages import RUTDPages

class LoadServer(WebPage):
    def start_lotba(self):
        """
        Pagina inicial /
        :return: pagina completa
        """
        end = "</body>\n</html>\n"
        mes = "202212"
        body = 'Carga históricos LOTBA\n'
        if not AppData.icConnected():
            body += '<p class="error">%s</p>\r\n' % "ERROR DE conexión: BBDD no accesible"
        else:
            body += '<p></p\r\n'
        body += '<ul>\n'
        body += '<li>RU: Registro de Usuario: Diario/Mensual\n\t<ul>\n'
        body += '\t<li><a href="/RUD_D">RUD Por jugador (diario)</a>\n'
        body += '\t<li><a href="/RUD_M">RUD Por jugador (mensual)</a>\n'
        body += '\t<li><a href="/RUT_D">RUT Totales (diario)</a>\n'
        body += '\t<li><a href="/RUT_M"></a>RUT Totales (mensual)\n'
        body += '\t</ul>\n'
        body += '<li>CJ: Cuenta de Juego\n\t<ul>\n'
        body += '</ul>\n'
        body += '<li>AJL: Agencia de Juego en Linea\n\t<ul>\n'
        body += '\t<li><a href=""></a>ACT: Cuenta de Agencia de Juegos en Línea (totales)\n'
        body += '\t<ul>\n'
        body += '\t\t<li><a href=""></a>ACT\n'
        body += '\t\t<li><a href=""></a>Apuestas\n'
        body += '\t\t<li><a href=""></a>Apuestas devolucion\n'
        body += '\t\t<li><a href=""></a>Comision\n'
        body += '\t\t<li><a href=""></a>Pozos\n'
        body += '\t\t<li><a href=""></a>Premios\n'
        body += '\t\t<li><a href=""></a>Otros\n'
        body += '\t</ul>\n'
        body += '\t<li><a href=""></a>CPT: Cuenta de Pozos y Partidas Vivas (totales).\n'
        body += '</ul>\n'
        body += '<li>JU: Juego\n\t<ul>\n'
        body += '</ul>\n'
        body += '<br>\n'
        return self.head("LOTBA: Carga historicos") + body + end

app = Flask(__name__)

@app.route('/')
def start_lotba():
    return LoadServer().start_lotba()

@app.route('/RUD_D')
def show_RUD_D():
    return RUDPages().show_RUD_D()

@app.route('/RUD_D_Mes/<mes>/<cargar>')
def show_RUD_D_Mes(mes, cargar="No"):
    return RUDPages().show_RUD_D_Mes(mes, cargar)

@app.route('/RUD_D_LoadXml/<mes>/<fName>')
def show_RUD_D_LoadXml(mes, fName):
    return RUDPages().show_RUD_D_LoadXml(mes, fName)

@app.route('/RUD_M')
def show_RUD_M():
    return RUMPages().show_RUD_M()

@app.route('/RUD_M_Mes/<mes>/<cargar>')
def show_RUD_M_Mes(mes, cargar="No"):
    return RUMPages().show_RUD_M_Mes(mes, cargar)

@app.route('/RUD_M_LoadXml/<mes>/<fName>')
def show_RUD_M_LoadXml(mes, fName):
    return RUMPages().show_RUD_M_LoadXml(mes, fName)

@app.route('/RUT_D')
def show_RUT_D():
    return RUTDPages().show_RUT_D()

@app.route('/RUT_D_Mes/<mes>/<cargar>')
def show_RUT_D_Mes(mes, cargar="No"):
    return RUTDPages().show_RUT_D_Mes(mes, cargar)
