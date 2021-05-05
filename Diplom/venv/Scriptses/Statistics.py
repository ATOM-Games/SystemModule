from datetime import datetime
from Scriptses.DataBase import *
from Particle.head import getHead
from Particle.header import header

dayOfWeek = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
	
def getToDayStatistics(db, ip, port):
	sts = getIPport(db, ip, port, "-")
	str_html = """<div id="stat"><h1>Статистика пользователя за сегодня</h1>"""
	if sts==[] :
		str_html+="""<h2>Критических ситуаций за сегодня не наблюдалось<h2>"""
	else :
		str_html+="<table id='sttb'><tr><td><b>Время</b></td><td><b>Ситуация</b></td></tr>"
		for row in sts:
			str_html+=("<tr><td>"+row['Time']+"</td><td>"+row['Situation']+"</td></tr>")
		str_html+="""</table>
			<table><tr><td width="200px"><input type="button" value="за все время" onclick="updateStat('all')" class="b_hed"/></td><td></td></tr></table>
		</div>"""
	return str_html
	
def getAllStatistics(db,ip, port):
	dt = str(datetime.now().day)+"."+str(datetime.now().month)+"."+str(datetime.now().year)
	sts = getIPport(db, ip, port, dt)
	str_html = """<div id="stat"><h1>Статистика пользователя за все время</h1>"""
	if sts==[] :
		str_html+="""<h2>Критических ситуаций за все время не наблюдалось<h2>"""
	else :
		str_html+="<table id='sttb'><tr><td><b>Дата</b></td><td><b>Время</b></td><td><b>Ситуация</b></td></tr>"
		for row in sts:
			str_html+=("<tr><td>"+row['Date']+"</td><td>"+row['Time']+"</td><td>"+row['Situation']+"</td></tr>")
		str_html+="""</table>
			<table><tr><td width="200px"><input type="button" value="за сегодня" onclick="updateStat('now')" class="b_hed"/></td><td></td></tr></table>
		</div>"""
	return str_html
	
def addCrit(db, ip, port):
	dt = str(datetime.now().day)+"."+str(datetime.now().month)+"."+str(datetime.now().year)
	tm = str(datetime.now().hour)+"."+str(datetime.now().minute)
	return addCritdb(db, ip, port, dt, tm, "Потеря сознания")
	
def admin_statistic(db, Log, who):
	str_html = getHead("Администратор")
	str_html += header(Log)
	str_html += """<div id="sts"><h1>Статистика администратора</h1><table id='usersts'><tr><td width="40%">"""
	users = getUserAll(db)
	i = 0
	str_html += ("""<input type='button' class='mb' onclick="window.location.href='/statistics'" value='Вся статистика'/>""")
	for user in users:
		i+=1
		str_html += ("""<input type='button' class='mb' onclick="window.location.href='/statistics?Id="""+user['Login']+"""'" value='"""+str(i)+"	"+user['Login']+"  :  "+user['First_name']+" "+user['Last_name']+"""'/>""")
	str_html += """</td><td id="as">"""
	str_html += stat_ad(db, who)
	str_html += """</td></tr><tr><td>
	<br/><br/><br/><br/><br/><input type="button" onclick="window.location.href='/registrate'" class="b_hed" value="Создать еще администратора"/>
	</td><td></td></tr></table>"""
	return str_html

def stat_ad(db, ad):
	str_html="<table id='sttb'><tr><td><b>Дата</b></td><td><b>Время</b></td><td><b>Событие</b></td><tr>"
	sts = ad_stat(db, ad)
	if sts==[]:
		str_html+="<tr><td colspan='3'><i>Статистика пуста</i></td></tr>"
	else :
		for st in sts:
			str_html+="<tr><td>"+st['Date']+"</td><td>"+st['Time']+"</td><td>"+st['Event']+"</td></tr>"
	str_html+="</table>"
	return str_html
	
	
	