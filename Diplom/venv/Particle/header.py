from flask import request

def header(U_L):
	head = "<header>"
	if U_L :
		head += """<form method="POST" action="/admin" style="margin:0">
					<table class="hed_t"><tr><td width=225px><h3>DispatcherControl</h3></td>
					<td width=250px>"""
		if request.path=="/statistics":
			head += """<input type="button" onclick="window.location.href='/admin'" class="hb_hed" value="Панель администратора"/>"""
		else :
			head += """<input type="button" onclick="window.location.href='/statistics'" class="hb_hed" value="Статистика администратора"/>"""
		head += """</td>
					<td></td>
                    <td width=250px><input type="submit" name="Admine_Logout" value="Выход" class="hb_hed"/></td>
					</tr></table>
                </form>"""
	else:
		head += """<table class="hed_t"><tr><td width=225px><h3>DispatcherControl</h3></td><td><h3> Вход </h3></td><td width=250px></td></tr></table>"""
	head +="</header>"
	return head