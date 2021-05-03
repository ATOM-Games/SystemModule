from Scriptses.DataBase import getUserByLogin
from Particle.head import getHead
from Particle.header import header
from Particle.Admin_videoBlock import getVideoBlock
from Particle.Admin_CameraList import getListOfCam
from Particle.Admin_panel import *

#from Scriptses.Socket_server import createSocket

def adregistrate(db, Log):
    str_html = getHead("Регистрация")
    str_html += header(Log)
    user = getUserByLogin(db, Log)
    user = getUserByLogin(db, Log)
    str_html += """<div class="cb cb_gray"><h1>Регистрация нового администратора</h1>"""
    str_html += """<form action="" method="POST" class="fm">
		<input type="text" class="cbi" placeholder="введите фамилию" name="new_fm" required/>
		<input type="text" class="cbi" placeholder="введите имя" name="new_nm" required/>
		<input type="text" class="cbi" placeholder="введите логин" name="new_lg" required/>
		<input type="password" class="cbi" placeholder="введите пароль" name="new_ps" required/>
		<p></p>
		<table width="100%"><tr>
			<td width="33%"><input type="reset" class="b_hed" value="Очистить поля"/></td>
			<td width="33%"><input type="button" class="b_hed" value="Отмена" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
			<td width="33%"><input type="submit" class="b_hed" value="Зарегистрировать" name="OK"/></td>
		</tr></table>
		</form></div>"""
    return str_html
	
def p_adregistrate(db, Log, n_lg, n_nm, n_fm, n_ps, err):
    str_html = getHead("Регистрация")
    str_html += header(Log)
    user = getUserByLogin(db, Log)
    user = getUserByLogin(db, Log)
    str_html += """<div class="cb """
    if err=="" :
        str_html += """cb_gren"><h1>Регистрация нового администратора</h1>
								<h1>Регистрация прошла успешно</h1>
								<p></p>
								<table width="100%"><tr>
									<td width="33%"></td>
									<td width="34%"><input type="button" class="b_hed" value="Панель администратора" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
									<td width="33%"></td>
								</tr></table>"""
    else :
        str_html += """cb_red"><h1>Регистрация нового администратора</h1>
								<h1>Ошибка</h1>
								<form action="" method="POST" class="fm"><h2>"""
        x = err.split("|")
        i = 1
        for e in x:
            str_html += "<p>"+str(i)+" "+e+"</p>"
            i=i+1
        str_html += """</h2>
			<input type="text" class="cbi" placeholder="введите фамилию" name="new_fm" value='"""+n_fm+"""' />
			<input type="text" class="cbi" placeholder="введите имя" name="new_nm" value='"""+n_nm+"""' />
			<input type="text" class="cbi" placeholder="введите логин" name="new_lg" value='"""+n_lg+"""' />
			<input type="password" class="cbi" placeholder="введите пароль" name="new_ps" value='"""+n_ps+"""' />
			<p></p>
		<table width="100%"><tr>
			<td width="33%"><input type="reset" class="b_hed" value="Очистить поля"/></td>
			<td width="33%"><input type="button" class="b_hed" value="Отмена" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
			<td width="33%"><input type="submit" class="b_hed" value="Зарегистрировать" name="OK"/></td>
		</tr></table></form>"""
    return str_html