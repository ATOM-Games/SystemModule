from Scriptses.DataBase import getUserByLogin
from Particle.head import getHead
from Particle.header import header
from Particle.Admin_videoBlock import getVideoBlock
from Particle.Admin_CameraList import getListOfCam
from Particle.Admin_Sittings import *
from Particle.Admin_ListenerList import getListOfList
from Particle.Admin_panel import *
from Scriptses.Statistics import *


#from Scriptses.Socket_server import createSocket

def administr(db, Log):
    str_html = getHead("Администратор")
    str_html += header(Log)
    user = getUserByLogin(db, Log)
    str_html += """<h1 style="text-align:center">"""+user[0]["First_name"]+""" """+user[0]["Last_name"]+"""</h1>"""
    str_html += ("""<table class='admin_t'>
	<tr><td><h2 id="c_s" class="s_h2">состояние подключения</h2></td><td><input type='button' value="Камеры" onclick="DisplayPanel('cam')" class="b_hed"/></td><td><input type='button' value="Слушатели" onclick="DisplayPanel('list')" class="b_hed"/></td><td><input type='button' value="Настройки" onclick="DisplayPanel('nas')" class="b_hed"/></td></tr>
	<tr><td>"""+getVideoBlock()+"""</td><td colspan="3" class='list_c'>"""+getListOfCam(db)+getListOfList(db)+getSittings()+"""</td></tr></table>"""+getAdmin()+"<br/><div id='sts'></div>")
    return str_html