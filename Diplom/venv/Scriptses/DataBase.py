import pymysql.cursors

DataBaseCon = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='',
                             db='diplom',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def getUserByLogin(db, userLogin):
    res = []
    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM users WHERE Login='"+userLogin+"'"
            cursor.execute(sql)
            for row in cursor:
                res.append(row)
    finally:
        # DataBaseCon.close()
        print("ERROR")
    return res

def getUserAll(db):
    res = []
    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            for row in cursor:
                res.append(row)
    finally:
        # DataBaseCon.close()
        print("ERROR")
    return res
	
	
def getCameraList(db):
    res = []
    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM cameras"
            cursor.execute(sql)
            for row in cursor:
                res.append(row)
    finally:
        # DataBaseCon.close()
        print("ERROR")
    return res

def checkCamera(db, id, ip, pt):
    res = []
    try:
        with db.cursor() as cursor:
            #sql = "Select * From cameras WHERE ID='"+id+"' AND IP_address='"+ip+"' AND PORT='"+pt+"'"
            sql = "Select * From cameras WHERE IP_address='" + ip + "' AND PORT='" + pt + "'"
            cursor.execute(sql)
            for row in cursor: res.append(row)
            if res==[] : return "null"
            else :
                if res[0]["cam_is_allowed"]=="0" : return "don't allow"
                else :
                    if res[0]["cam_is_running"] == "1": return "is_running"
                    else : return "good"
    finally:
        print("ERROR")
    return "Other error"

def stateCamera(db, id, ip, pt, state):
    res = []
    try:
        with db.cursor() as cursor:
            #sql = "UPDATE cameras SET cam_is_running = '"+state+"' WHERE ID = '"+id+"'"
            sql = "UPDATE cameras SET cam_is_running = '" + state + "' WHERE IP_address='" + ip + "' AND PORT='" + pt + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            db.commit()
            print(result)
            return "good"
    finally:
        print("ERROR")
    return "Other error"

def addCamera(db, Log, ip, pt):
    res = []
    try:
        with db.cursor() as cursor:
            #sql = "INSERT INTO cameras (IP_address, PORT, cam_is_running, cam_is_allowed) VALUES ('"+ip+"', '"+pt+"', '0', '1')"
            sql = "CALL addCamera ('"+ip+"', "+pt+", '"+Log+"')"
            cursor.execute(sql)
            result = cursor.fetchone()
            db.commit()
            print(result)
            return "good"
    finally:
        print("ERROR")
    return "Other error"

def editCamera(db, Log, id, new_ip, new_pt):
    res = []
    try:
        with db.cursor() as cursor:
            #sql = "INSERT INTO cameras (IP_address, PORT, cam_is_running, cam_is_allowed) VALUES ('"+ip+"', '"+pt+"', '0', '1')"
            sql = "CALL editCamera("+id+", '"+new_ip+"', "+new_pt+", '"+Log+"')"
            cursor.execute(sql)
            result = cursor.fetchone()
            db.commit()
            print(result)
            return "good"
    finally:
        print("ERROR")
    return "Other error"

def deleteCamera(db, Log, id):
    res = []
    try:
        with db.cursor() as cursor:
            #sql = "INSERT INTO cameras (IP_address, PORT, cam_is_running, cam_is_allowed) VALUES ('"+ip+"', '"+pt+"', '0', '1')"
            cam = getCamera(db, id)
            sql = "CALL deleteCamera("+id+", '"+cam[0]['IP_address']+"', "+cam[0]['PORT']+", '"+Log+"')"
            cursor.execute(sql)
            result = cursor.fetchone()
            db.commit()
            print(result)
            return "good"
    finally:
        print("ERROR")
    return "Other error"

def getCamera(db, id):
    res = []
    try:
        with db.cursor() as cursor:
            sql = "Select * From cameras WHERE ID = '" + id + "'"
            cursor.execute(sql)
            for row in cursor: res.append(row)
            return res
    finally:
        print("ERROR")
    return "Other error"
	
def registraition(db, Log, lgin, nme, fml, passs):
	err = ""
	if lgin == "" or lgin == None :
		err += "Введите логин"
	if nme == "" or nme == None :
		if err != "" : err += "|"
		err += "Введите имя"
	if fml == "" or fml == None :
		if err != "" : err += "|"
		err += "Введите фамилию"
	if passs == "" or passs == None :
		if err != "" : err += "|"
		err += "Введите пароль"
	if lgin != "" :
		if getUserByLogin(db, lgin)!=[] :
			if err != "" : err += "|"
			err += "Пользователь с логином '"+lgin+"' уже есть"
		else :
			if nme != "" and fml != "" and passs != "" :
				try:
					with db.cursor() as cursor:			
						sql = "CALL RegistrateUser('"+lgin+"', '"+fml+"', '"+nme+"', '"+passs+"', '"+Log+"')"
						cursor.execute(sql)
						result = cursor.fetchone()
						db.commit()
				finally:
					print("ERROR")
	if err == "" and getUserByLogin(db, lgin)==[] :
		err += "Проблема с соединением! Повторите попытку позже"
	return err

#статистика
def getIPport(db, ip, port, datetime):
	sql = "Select * From crit_situation WHERE IP = '" + ip + "' AND PORT='"+port+"'"
	if datetime!="-":
		sql += " AND Date='"+datetime+"'"
	res = []
	try:
		with db.cursor() as cursor:
			cursor.execute(sql)
			for row in cursor:
				res.append(row)
	finally:
		# DataBaseCon.close()
		print("ERROR")
	return res

def addCritdb(db, ip, port, date, time, situation):
	res = []
	try:
		with db.cursor() as cursor:
			sql = "CALL add_crit_situation('"+ip+"', '"+port+"', '"+date+"', '"+time+"', '"+situation+"')"
			cursor.execute(sql)
			result = cursor.fetchone()
			db.commit()
			print(result)
			return "good"
	finally:
		print("ERROR")
	return "Other error"

def ad_stat(db, ad):
	res=[]
	sql = "Select * From admin_statistics"
	if ad!="" : sql += " WHERE Login='"+ad+"'"
	try:
		with db.cursor() as cursor:
			cursor.execute(sql)
			for row in cursor:
				res.append(row)
	finally:
        # DataBaseCon.close()
		print("ERROR")
	return res
	
#--------------
def addListener(db, Log, ip, pt):
    res = []
    try:
        with db.cursor() as cursor:
            sql = "CALL add_listener ('"+ip+"', "+pt+", '"+Log+"')"
            cursor.execute(sql)
            result = cursor.fetchone()
            db.commit()
            print(result)
            return "good"
    finally:
        print("ERROR")
    return "Other error"

def editListener(db, Log, id, new_ip, new_pt):
    res = []
    try:
        with db.cursor() as cursor:
            sql = "CALL edit_listener("+id+", '"+new_ip+"', "+new_pt+", '"+Log+"')"
            cursor.execute(sql)
            result = cursor.fetchone()
            db.commit()
            print(result)
            return "good"
    finally:
        print("ERROR")
    return "Other error"

def deleteListener(db, Log, id):
    res = []
    try:
        with db.cursor() as cursor:
            lists = getListener(db, id)
            sql = "CALL delete_listener("+id+", '"+lists[0]['IP_address']+"', "+lists[0]['PORT']+", '"+Log+"')"
            cursor.execute(sql)
            result = cursor.fetchone()
            db.commit()
            print(result)
            return "good"
    finally:
        print("ERROR")
    return "Other error"

def getListener(db, id):
    res = []
    try:
        with db.cursor() as cursor:
            sql = "Select * From listener WHERE ID = '" + id + "'"
            cursor.execute(sql)
            for row in cursor: res.append(row)
            return res
    finally:
        print("ERROR")
    return "Other error"

def getListenerList(db):
    res = []
    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM listener"
            cursor.execute(sql)
            for row in cursor:
                res.append(row)
    finally:
        # DataBaseCon.close()
        print("ERROR")
    return res