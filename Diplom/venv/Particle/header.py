

def header(U_L):
    head = "<header>"
    if U_L :
        head += """<form method="POST" action="/admin" style="margin:0">
					<table class="hed_t"><tr>
					<td width=250px><input type="button" onclick="window.location.href='/registrate'" class="b_hed" value="Создать еще администратора"/></td>
					<td></td>
                    <td  width=250px><input type="submit" name="Admine_Logout" value="LogOut" class="b_hed"/></td>
					</tr></table>
                </form>"""
    else:
        head += """<h3> Вход </h3>"""

    head +="</header>"
    return head