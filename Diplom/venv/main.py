import onnx
from flask import Flask, jsonify, request, make_response, render_template
from Scriptses.DataBase import *
from Scriptses.Login import login, logout
from Scriptses.Administate import administr
from Particle.Admin_CID_Cam import *
from Scriptses.Registarte import *

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
            res = addCamera(DataBaseCon, request.form['Ip_new_cam'], request.form['Port_new_cam'])
            return get_create_Result(U_L)
        if request.form.get('Edit_cam'):
            res = editCamera(DataBaseCon, request.form['Id_cam'], request.form['Ip_cam'], request.form['Port_cam'])
            return get_edit_Result(U_L)
        if request.form.get('Delete_cam'):
            res = deleteCamera(DataBaseCon, request.form['Id_cam'])
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
	err = registraition(DataBaseCon, l, n, f, p)
	return p_adregistrate(DataBaseCon, U_L, l, n, f, p, err)
	
#ошибка 404
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)