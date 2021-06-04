from flask import Flask, jsonify, request, make_response, render_template
from flask_cors import CORS

params = dict()

for line in open("ServerConfig.cfg", "r").readlines():
    p_name, p_val = line.split("=")
    params[p_name.strip()] = p_val.strip()

app = Flask(__name__)
CORS(app)



@app.route('/')
def index():
	report = dict()
	for line in open("report.cfg", "r").readlines():
		p_nme, p_vl = line.split("=")
		report[p_nme.strip()] = p_vl.strip()
	html_str=""
	if report==dict() :
		html_str+= "<h1>Слушатель готов</h1>"
	else :
		html_str+= """<h1>Отчет</h1>
		<table style="border-collapse : collapse;">
		<tr><td style="border : 1px solid #000; padding : 5px;">Дата</td><td style="border : 1px solid #000; padding : 5px;">"""+report['dates']+"""</td></tr>
		<tr><td style="border : 1px solid #000; padding : 5px;">Время</td><td style="border : 1px solid #000; padding : 5px;">"""+report['times']+"""</td></tr>
		<tr><td style="border : 1px solid #000; padding : 5px;">Пользователь</td><td style="border : 1px solid #000; padding : 5px;">"""+report['user']+"""</td></tr>
		<tr><td style="border : 1px solid #000; padding : 5px;">Событие</td><td style="border : 1px solid #000; padding : 5px;">"""+report['mess']+"""</td></tr>
		</table></br><input type="button" value="Очистить отчет" onclick="clearReport('"""+params["address"]+"""','"""+params["port"]+"""')" style="display : block; padding : 10px; width : 200px; font-weight : bold; color : 000; background-color : #fff; text-decoration : none; text-align : center; border : 1px solid #111; border-radius : .3rem; box-shadow  : 0 0 0px #555;"/>"""
	html_str +="""<script src="static/jQuery3.js"></script><script type="text/javascript" src="static/Script.js"></script>"""
	return html_str
	
@app.route('/clear', methods=['POST'])
def index_c():
	report = request.get_json(force=True)['clear']
	f = open('report.cfg', 'w')
	f.write('')
	f.close()
	return jsonify({"message": "good"})
	
@app.route('/poct', methods=['POST'])
def index_p():
	str = ['dates = '+request.get_json(force=True)['dates'],
	'times = '+request.get_json(force=True)['times'],
	'user = '+request.get_json(force=True)['user'],
	'mess = '+request.get_json(force=True)['mess']]
	f = open('report.cfg', 'w')
	for index in str: f.write(index + '\n')
	f.close()
	return jsonify({"message": "good"})

	
	
	
if __name__ == '__main__':
    app.run(host=params["address"], port=params["port"], debug=bool(params["debug"]))