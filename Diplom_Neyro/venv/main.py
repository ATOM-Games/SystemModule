from flask import Flask, jsonify, request, make_response, render_template, json
from flask_cors import CORS
from Asker import *
import base64
from PIL import Image
import cv2
#from Predict import *

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
params = dict()

for line in open("ServerConfig.cfg", "r").readlines():
    p_name, p_val = line.split("=")
    params[p_name.strip()] = p_val.strip()

app = Flask(__name__)

#scope = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/qwerty')
def qwerty(): return "qwerty"

@app.route('/face_detect', methods=['POST'])
def face_detect():
    wstr = request.get_json(force=True)['dates']
    img = base64.b64decode(wstr)
    rezlt = ask_face(img)
    return jsonify({"message": rezlt })

@app.route('/isface_detect', methods=['POST'])
def isface_detect():
    wstr = request.get_json(force=True)['dates']
    img = base64.b64decode(wstr)
    rezlt = ask_isface(img)
    return jsonify({"message": rezlt })

@app.route('/isbody_detect', methods=['POST'])
def isbody_detect():
    wstr = request.get_json(force=True)['dates']
    img = base64.b64decode(wstr)
    rezlt = ask_body(img)
    if rezlt == None :
        return jsonify({"message": "None"})
    else :
        return jsonify({"message": rezlt[0]+" "+rezlt[1]+" "+rezlt[2]})

all_states = ['Лицо', 'Тело', 'Встал', 'Сел', 'Ушел', 'Отсутствует', 'Пришел', 'Пропал', 'Потеря сознания']


@app.route('/isuniverce_detect', methods=['POST'])
def isuniverce_detect():
    wstr = request.get_json(force=True)['dates']
    states = [request.get_json(force=True)['bf1'],
              request.get_json(force=True)['bf2'],
              request.get_json(force=True)['bf3'],
              request.get_json(force=True)['bf4'],
              request.get_json(force=True)['bf5']]
    img = base64.b64decode(wstr)
    result = analysOfState(ask_isface(img), ask_body(img), states)
    return jsonify({ "message": result })

def analysOfState(face, body, last_state):
    if last_state[4] == '-' : # подготовка к анализу
        return nowState(face, body)
    else : # анализ
        if last_state[0] == all_states[0] or last_state[0] == all_states[3] : # если раньше было видно лицо...
            if nowState(face, body) == all_states[0] : # и оно остается
                return all_states[0] # то оно остается
            if nowState(face, body) == all_states[1] : # вдруг пропало лицо но тело осталось
                return all_states[2] # то человек встал
            if nowState(face, body) == all_states[5] : # вдруг пропал полностью пользователь
                return all_states[7]  # то человек пропал
        if last_state[0] == all_states[1] or last_state[0] == all_states[2] or last_state[0] == all_states[6] :
            if nowState(face, body) == all_states[0] : # появляется лицо
                return all_states[3] # сел
            if nowState(face, body) == all_states[1] : # зачем-то долго стоит перед камерой
                return all_states[1]
            if nowState(face, body) == all_states[5] : # ушел куда-то
                return all_states[4]
        if last_state[0] == all_states[4] or last_state[0] == all_states[5] : # ушел куда-то
            if nowState(face, body) == all_states[0]:  # появляется лицо
                return all_states[3]
            if nowState(face, body) == all_states[1] :
                return all_states[6]
            if nowState(face, body) == all_states[5] :
                return all_states[4]
        if last_state[0] == all_states[7] :
            if nowState(face, body) == all_states[0]:  # появляется лицо
                return all_states[3]
            if nowState(face, body) == all_states[1] :
                return all_states[6]
            if nowState(face, body) == all_states[5] :
                if last_state[1] == all_states[7] and last_state[2] == all_states[7] and last_state[3] == all_states[7] and last_state[4] == all_states[7] :
                    return all_states[8]
                else :
                    return all_states[7]
        if last_state[0] == all_states[8] :
            if nowState(face, body) == all_states[0]:  # появляется лицо
                return all_states[3]
            if nowState(face, body) == all_states[1] :
                return all_states[6]
            if nowState(face, body) == all_states[5] :
                return all_states[8]
    return all_states[5] #непонятка

def nowState(face, body):
    if face: return all_states[0]
    else:
        if body: return all_states[1]
        else: return all_states[5]

if __name__ == '__main__':
    app.run(host=params["address"], port=params["port"], debug=bool(params["debug"]))