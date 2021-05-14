from flask import request

def header(U_L):
	head = "<header>"
	if U_L :
		head += """<form method="POST" action="/admin" style="margin:0">
					<table class="hed_t"><tr>
					<td width=250px>"""
		if request.path=="/statistics":
			head += """<input type="button" onclick="window.location.href='/admin'" class="b_hed" value="Панель администратора"/>"""
		else :
			head += """<input type="button" onclick="window.location.href='/statistics'" class="b_hed" value="Статистика администратора"/>"""
		head += """</td>
					<td></td>
                    <td  width=250px><input type="submit" name="Admine_Logout" value="Выход" class="b_hed"/></td>
					</tr></table>
                </form>"""
	else:
		head += """<h3> Вход </h3>"""
	head +="</header>"
	return head