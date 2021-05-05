from Scriptses.DataBase import getUserByLogin
from Particle.head import getHead
from Particle.header import header
from Particle.Admin_videoBlock import getVideoBlock
from Particle.Admin_CameraList import getListOfCam
from Particle.Admin_panel import *
from Scriptses.Statistics import *

#from Scriptses.Socket_server import createSocket

def administr(db, Log):
    str_html = getHead("Администратор")
    str_html += header(Log)
    user = getUserByLogin(db, Log)
    str_html += """<h1>"""+user[0]["First_name"]+""" """+user[0]["Last_name"]+"""</h1>"""
    str_html += ("""<table class='admin_t'>
	<tr><td colspan="2"><h2 id="c_s" class="s_h2">состояние подключения</h2></td><td rowspan="2" class='list_c'>"""+getListOfCam(db)+"""</td></tr>
	<tr><td>"""+getVideoBlock()+"</td></tr></table>"+getAdmin()+"<br/><div id='sts'></div>")
    return str_html