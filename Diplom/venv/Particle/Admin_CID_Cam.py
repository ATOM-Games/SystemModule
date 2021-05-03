from Scriptses.DataBase import *
from Particle.head import getHead
from Particle.header import header
from Particle.Admin_CameraList import *
from Scriptses.DataBase import *

def get_default_Forms(U_L):
    htlm = getHead("Работа с камерами") + header(U_L)
    htlm += """<div class="cb cb_gray">
		<h1>работа с камерами</h1>
		<p></p>
		<div style="margin:0 auto; width:400px">"""
    htlm += getListOfCam(DataBaseCon)
    htlm += """</div></div>"""
    return htlm


# создание новой камеры
def get_create_Forms(U_L):
    htlm = getHead("Новая камера") + header(U_L)
    htlm += """
	<div class="cb cb_gray">
		<h1>Новая камера</h1>
		<form action="/CID_Cam" method="POST" class="fm">
			<input type="text" class="cbi" placeholder="ip-адресс камеры" name="Ip_new_cam" required pattern="^([0-9]{1,3}\.){3}[0-9]{1,3}$"/>
			<input type="number" class="cbi" placeholder="порт камеры" name="Port_new_cam" min="1000" required />
			<p></p>
			<table width="100%"><tr>
			<td width="50%"><input type="button" class="b_hed" value="Отмена" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
			<td width="50%"><input type="submit" class="b_hed" value="Зарегистрировать камеру" name="Reg_cam"/></td>
			</tr></table>
		</form>
	</div>"""
    return htlm

def get_create_Result(U_L):
    htlm = getHead("Новая камера") + header(U_L)
    htlm += """
	<div class="cb cb_gren">
        <h1>Камера зарегестрирована успешно</h1>
		<p></p>
        <table width="100%"><tr>
			<td width="33%"></td>
			<td width="34%"><input type="button" class="b_hed" value="Панель администратора" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
			<td width="33%"></td>
		</tr></table>
	</div>
    """
    return htlm

# редактирование камеры по ID
def get_edit_Form(U_L, ID, old_ip, old_port):
    htlm = getHead("Редактирование камеры") + header(U_L)
    htlm += """
		<div class="cb cb_gray">
			<h1>Редактирование камеры</h1>
			<form action="/CID_Cam" method="POST" class="fm">
				<input type="hidden" placeholder="ip-адресс камеры" name="Id_cam" value='"""+ID+"""'/>
				<input type="text" class="cbi" placeholder="ip-адресс камеры" name="Ip_cam" value='"""+old_ip+"""' required pattern="^([0-9]{1,3}\.){3}[0-9]{1,3}$"/>
				<input type="number" class="cbi" placeholder="порт камеры" name="Port_cam" value='"""+old_port+"""' required/>
				<p></p>
				<table width="100%"><tr>
				<td width="50%"><input type="button" class="b_hed" value="Отмена" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
				<td width="50%"><input type="submit" class="b_hed" value="Отредактировать камеру" name="Edit_cam"/></td>
				</tr></table>
			</form>
		</div>
        """
    return htlm

def get_edit_Result(U_L):
    htlm = getHead("Редактирование камеры") + header(U_L)
    htlm += """
        <div class="cb cb_gren">
        <h1>Камера отредактирована успешно</h1>
		<p></p>
        <table width="100%"><tr>
			<td width="33%"></td>
			<td width="34%"><input type="button" class="b_hed" value="Панель администратора" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
			<td width="33%"></td>
		</tr></table>
	</div>
    """
    return htlm

# удаление камеры по ID
def get_delit_Form(U_L, ID, old_ip, old_port):
    htlm = getHead("Удаление камеры") + header(U_L)
    htlm += """
	<div class="cb cb_red">
    <h1>Вы действительно хотите удалить камеру """+old_ip+":"+old_port+"""</h1>
        <form action="/CID_Cam" method="POST">
            <input type="hidden" placeholder="ip-адресс камеры" name="Id_cam" value='"""+ID+"""'/>
            <input type="hidden" placeholder="ip-адресс камеры" name="Ip_cam" value='"""+old_ip+"""'/>
            <input type="hidden" placeholder="порт камеры" name="Port_cam" value='"""+old_port+"""'/>
			<p></p>
				<table width="100%"><tr>
				<td width="50%"><input type="button" class="b_hed" value="Отмена" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
				<td width="50%"><input type="submit" class="b_hed" value="Удалить камеру" name="Delete_cam"/></td>
			</tr></table>
        </form>
	</div>"""
    return htlm

def get_delete_Result(U_L):
    htlm = getHead("Удаление камеры") + header(U_L)
    htlm += """
		<div class="cb cb_gren">
			<h1>Камера удалена успешно</h1>
			<p></p>
			<table width="100%"><tr>
				<td width="33%"></td>
				<td width="34%"><input type="button" class="b_hed" value="Панель администратора" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
				<td width="33%"></td>
			</tr></table>
		</div>"""
    return htlm