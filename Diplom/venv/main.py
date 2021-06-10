import onnx
from flask import Flask, jsonify, request, make_response, render_template
from Scriptses.DataBase import *
from Scriptses.Login import login, logout
from Scriptses.Administate import administr
from Particle.Admin_CID_Cam import *
from Particle.Admin_CID_List import *
from Scriptses.Registarte import *
from Scriptses.Statistics import *

import websockets as ws
import asyncio

app = Flask(__name__)

@app.route('/')
def index():
    U_L = request.cookies.get('USER_LOGIN')
    if U_L :
        return administr(DataBaseCon, U_L)
    else :
        return login(DataBaseCon, "", "", U_L)

#вход на сайт
@app.route('/login')
def mlogin():
    U_L = request.cookies.get('USER_LOGIN')
    return login(DataBaseCon, "", "", U_L)

@app.route('/login', methods=['POST'])
def mlogin_p():
    user_login = request.form.get('userLogin')
    user_password = request.form.get('userPassw')
    U_L = request.cookies.get('USER_LOGIN')
    return login(DataBaseCon, user_login, user_password, U_L)

@app.route('/registration')
def registration():
    return "<h1>Регистрация</h1>"

#админка
@app.route('/admin')
def admin():
    U_L = request.cookies.get('USER_LOGIN')
    if U_L :
        return administr(DataBaseCon, U_L)
    else :
        return login(DataBaseCon, "", "", U_L)

@app.route('/admin', methods=['POST'])
def admin_p():
    if request.form.get('Admine_Login') :
        lg = request.form.get('userLogin')
        str = administr(DataBaseCon, lg)
        res = make_response(str)
        res.set_cookie('USER_LOGIN', lg, max_age=60 * 60 * 24 * 365 * 2)
        return res
    if request.form.get('Admine_Logout') :
        str = login(DataBaseCon, "", "", None)
        res = make_response(str)
        res.set_cookie('USER_LOGIN', "", max_age=0)
        return res
    if request.form.get('SelectClientCam') :
        c_ip = request.form.get('IP_c')
        c_pt = request.form.get('Port_c')
        #createSocket(c_ip, c_pt)
        U_L = request.cookies.get('USER_LOGIN')
        str = administr(DataBaseCon, U_L)
        return str

@app.route('/check_camera', methods=['POST'])
def check_camera():
    err = checkCamera(DataBaseCon, request.form['id'], request.form['address'], request.form['port'])
    if err == "null" :
        return jsonify({"type": "error", "message": "Камера не была зарегестрирована администратором"})
    elif err == "don't allow" :
        return jsonify({"type": "error", "message": "Данные с камеры не допущены в обработку"})
    elif err == "is_running" :
        return jsonify({"type": "error", "message": "Данная камера уже запущена"})
    elif err == "Other error" :
        return jsonify({"type": "error", "message": "Возможно проблема с соединением"})
    return jsonify({"type": "success"})

@app.route('/run_camera', methods=['POST'])
def run_camera():
    res = stateCamera(DataBaseCon, request.form['id'], request.form['address'], request.form['port'], "1")
    return jsonify({"type": "success"})

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    res = stateCamera(DataBaseCon, request.form['id'], request.form['address'], request.form['port'], "0")
    return jsonify({"type": "success"})

@app.route('/CID_Cam')
def cid_Cam():
    U_L = request.cookies.get('USER_LOGIN')
    if request.method == 'GET':
        if request.args.get('Create') :
            return get_create_Forms(U_L)
        if request.args.get('Edit') :
            strd = ""+request.args.get('Edit')
            cam = getCamera(DataBaseCon, strd)[0]
            return get_edit_Form(U_L, str(cam['ID']), cam['IP_address'], str(cam['PORT']) )
        if request.args.get('Delete') :
            strd = "" + request.args.get('Delete')
            cam = getCamera(DataBaseCon, strd)[0]
            return get_delit_Form(U_L, str(cam['ID']), cam['IP_address'], str(cam['PORT']) )
    return get_default_Forms(U_L)

@app.route('/CID_Cam', methods=['POST'])
def cid_Cam_z():
    print("or POST or GET")
    U_L = request.cookies.get('USER_LOGIN')
    if request.method == 'POST':
        if request.form.get('Reg_cam'):
            res = addCamera(DataBaseCon, U_L, request.form['Ip_new_cam'], request.form['Port_new_cam'])
            return get_create_Result(U_L)
        if request.form.get('Edit_cam'):
            res = editCamera(DataBaseCon, U_L, request.form['Id_cam'], request.form['Ip_cam'], request.form['Port_cam'])
            return get_edit_Result(U_L)
        if request.form.get('Delete_cam'):
            res = deleteCamera(DataBaseCon, U_L, request.form['Id_cam'])
            return get_delete_Result(U_L)

@app.route('/registrate')
def registrate():
	U_L = request.cookies.get('USER_LOGIN')
	return adregistrate(DataBaseCon, U_L)

@app.route('/registrate', methods=['POST'])
def registrate_p():
	U_L = request.cookies.get('USER_LOGIN')
	f = request.form.get('new_fm')
	n = request.form.get('new_nm')
	l = request.form.get('new_lg')
	p = request.form.get('new_ps')
	err = registraition(DataBaseCon, U_L, l, n, f, p)
	return p_adregistrate(DataBaseCon, U_L, l, n, f, p, err)
	
@app.route('/statistics')
def statistics():
	U_L = request.cookies.get('USER_LOGIN')
	if request.method == 'GET':
		if request.args.get('Id') :
			return admin_statistic(DataBaseCon, U_L, request.args.get('Id'))
	return admin_statistic(DataBaseCon, U_L, "")
	
@app.route('/statistics', methods=['POST'])
def statistics_p():
	U_L = request.cookies.get('USER_LOGIN')
	if request.get_json(force=True)['sts']=='crit':
		l_ip = request.get_json(force=True)['l_ip']
		l_pt = request.get_json(force=True)['l_pt']
		if request.get_json(force=True)['dates']=='now':
			return jsonify({"message": getToDayStatistics(DataBaseCon, l_ip, l_pt)})
		else :
			return jsonify({"message": getAllStatistics(DataBaseCon, l_ip, l_pt)})
	if request.get_json(force=True)['sts']=='add_crit':
		l_ip = request.get_json(force=True)['l_ip']
		l_pt = request.get_json(force=True)['l_pt']
		rres = addCrit(DataBaseCon, l_ip, l_pt, request.get_json(force=True)['Situation'])
		return jsonify({"message": getToDayStatistics(DataBaseCon, l_ip, l_pt)})
	return jsonify({"message": "success"})
#----------
@app.route('/CID_List')
def cid_List():
    U_L = request.cookies.get('USER_LOGIN')
    if request.method == 'GET':
        if request.args.get('Create') :
            return get_create_Forms_list(U_L)
        if request.args.get('Edit') :
            strd = ""+request.args.get('Edit')
            cam = getListener(DataBaseCon, strd)[0]
            return get_edit_Form_list(U_L, str(cam['ID']).__str__(), cam['IP_address'], cam['Port'].__str__() )
        if request.args.get('Delete') :
            strd = "" + request.args.get('Delete')
            cam = getListener(DataBaseCon, strd)[0]
            return get_delit_Form_list(U_L, str(cam['ID']).__str__(), cam['IP_address'], cam['Port'].__str__() )
    return get_default_Forms_list(U_L)

@app.route('/CID_List', methods=['POST'])
def cid_List_z():
    print("or POST or GET")
    U_L = request.cookies.get('USER_LOGIN')
    if request.method == 'POST':
        if request.form.get('Reg_cam'):
            res = addListener(DataBaseCon, U_L, request.form['Ip_new_cam'], request.form['Port_new_cam'])
            return get_create_Result_list(U_L)
        if request.form.get('Edit_cam'):
            res = editListener(DataBaseCon, U_L, request.form['Id_cam'], request.form['Ip_cam'], request.form['Port_cam'])
            return get_edit_Result_list(U_L)
        if request.form.get('Delete_cam'):
            res = deleteListener(DataBaseCon, U_L, request.form['Id_cam'])
            return get_delete_Result_list(U_L)
#ошибка 404
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)