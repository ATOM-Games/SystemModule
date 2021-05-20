from Scriptses.DataBase import *
from Particle.head import getHead
from Particle.header import header
from Particle.Admin_ListenerList import *

def get_default_Forms_list(U_L):
    htlm = getHead("Работа со слушателями") + header(U_L)
    htlm += """<div class="cb cb_gray">
		<h1>работа со слушателями</h1>
		<p></p>
		<div style="margin:0 auto; width:400px">"""
    htlm += getListOfList(DataBaseCon)
    htlm += """</div></div>"""
    return htlm


# создание нового слушателя
def get_create_Forms_list(U_L):
    htlm = getHead("Новый слушатель") + header(U_L)
    htlm += """
	<div class="cb cb_gray">
		<h1>Новый слушатель</h1>
		<form action="/CID_List" method="POST" class="fm">
			<input type="text" class="cbi" placeholder="ip-адресс слушателя" name="Ip_new_cam" required pattern="^([0-9]{1,3}\.){3}[0-9]{1,3}$"/>
			<input type="number" class="cbi" placeholder="порт слушателя" name="Port_new_cam" min="1000" required />
			<p></p>
			<table width="100%"><tr>
			<td width="50%"><input type="button" class="b_hed" value="Отмена" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
			<td width="50%"><input type="submit" class="b_hed" value="Зарегистрировать слушателя" name="Reg_cam"/></td>
			</tr></table>
		</form>
	</div>"""
    return htlm

def get_create_Result_list(U_L):
    htlm = getHead("Новый слушатель") + header(U_L)
    htlm += """
	<div class="cb cb_gren">
        <h1>слушатель зарегестрирован успешно</h1>
		<p></p>
        <table width="100%"><tr>
			<td width="33%"></td>
			<td width="34%"><input type="button" class="b_hed" value="Панель администратора" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
			<td width="33%"></td>
		</tr></table>
	</div>
    """
    return htlm

# редактирование слушателя по ID
def get_edit_Form_list(U_L, ID, old_ip, old_port):
    htlm = getHead("Редактирование слушателя") + header(U_L)
    htlm += """
		<div class="cb cb_gray">
			<h1>Редактирование слушателя</h1>
			<form action="/CID_List" method="POST" class="fm">
				<input type="hidden" placeholder="ip-адресс слушателя" name="Id_cam" value='"""+ID+"""'/>
				<input type="text" class="cbi" placeholder="ip-адресс слушателя" name="Ip_cam" value='"""+old_ip+"""' required pattern="^([0-9]{1,3}\.){3}[0-9]{1,3}$"/>
				<input type="number" class="cbi" placeholder="порт слушателя" name="Port_cam" value='"""+old_port+"""' required/>
				<p></p>
				<table width="100%"><tr>
				<td width="50%"><input type="button" class="b_hed" value="Отмена" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
				<td width="50%"><input type="submit" class="b_hed" value="Отредактировать слушателя" name="Edit_cam"/></td>
				</tr></table>
			</form>
		</div>
        """
    return htlm

def get_edit_Result_list(U_L):
    htlm = getHead("Редактирование слушателя") + header(U_L)
    htlm += """
        <div class="cb cb_gren">
        <h1>Слушатель отредактирован успешно</h1>
		<p></p>
        <table width="100%"><tr>
			<td width="33%"></td>
			<td width="34%"><input type="button" class="b_hed" value="Панель администратора" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
			<td width="33%"></td>
		</tr></table>
	</div>
    """
    return htlm

# удаление слушателя по ID
def get_delit_Form_list(U_L, ID, old_ip, old_port):
    htlm = getHead("Удаление слушателя") + header(U_L)
    htlm += """
	<div class="cb cb_red">
    <h1>Вы действительно хотите удалить слушателя """+old_ip+":"+old_port+"""</h1>
        <form action="/CID_List" method="POST">
            <input type="hidden" placeholder="ip-адресс слушателя" name="Id_cam" value='"""+ID+"""'/>
            <input type="hidden" placeholder="ip-адресс слушателя" name="Ip_cam" value='"""+old_ip+"""'/>
            <input type="hidden" placeholder="порт слушателя" name="Port_cam" value='"""+old_port+"""'/>
			<p></p>
				<table width="100%"><tr>
				<td width="50%"><input type="button" class="b_hed" value="Отмена" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
				<td width="50%"><input type="submit" class="b_hed" value="Удалить слушателя" name="Delete_cam"/></td>
			</tr></table>
        </form>
	</div>"""
    return htlm

def get_delete_Result_list(U_L):
    htlm = getHead("Удаление слушателя") + header(U_L)
    htlm += """
		<div class="cb cb_gren">
			<h1>Слушатель удалена успешно</h1>
			<p></p>
			<table width="100%"><tr>
				<td width="33%"></td>
				<td width="34%"><input type="button" class="b_hed" value="Панель администратора" name="Reg_cam" onclick="window.location.href='/admin'"/></td>
				<td width="33%"></td>
			</tr></table>
		</div>"""
    return htlm