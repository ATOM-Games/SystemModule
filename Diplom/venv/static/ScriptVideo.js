var socket = null
var b_OnServer_FaceRecognize = false;
var b_OnServer_isFaceRecognize = false;
var b_OnServer_isBodyRecognize = false;
var b_OnServer_isUniverce = false;
var str_video="";

var l_ip="", l_pt="";
var lastCrit=false;

function messageSocket(cls, msg){
	document.getElementById('c_s').innerHTML = msg;
	document.getElementById('c_s').setAttribute('class', cls);
}

function createSocket(ip, pt){
	lastCrit=false;
    socket = new WebSocket("ws://"+ip+":"+pt);
	l_ip = ip; l_pt = pt;
	messageSocket('s_h2_y', 'Cоединение...');
	updateStat("now");
    socket.onopen = function() {
        //alert("Соединение установлено.");
		messageSocket('s_h2_g', 'Cоединение установлено');
        str_video="";
        b_OnServer_FaceRecognize = false;
        b_OnServer_isFaceRecognize = false;
		b_OnServer_isBodyRecognize = false;
        b_OnServer_isUniverce = false;
        clearstate();
    };
    socket.onclose = function(event) {
        if (event.wasClean) {
            //alert('Соединение закрыто чисто');
			messageSocket('s_h2_r', 'Cоединение закрыто');
        } else {
            //alert('Обрыв соединения'); // например, "убит" процесс сервера
			messageSocket('s_h2_r', 'Cоединение прервано');
        }
        //alert('Код: ' + event.code + ' причина: ' + event.reason);
		stop_monitoring();
		dont_tracking_face();
		str_video="";
		clearstate();
		setMessage('off');
    };
    socket.onmessage = function(event) {
        var video = document.getElementById("video_block");
        var reader = new FileReader();
        reader.readAsDataURL(event.data);
        reader.onload  = function() {
			str_video = atob(reader.result.replace('data:application/octet-stream;base64,', ''));
            video.src = "data:image/jpeg;base64," + str_video;
            console.log(new Date().getTime()/1000);
			
        }
    };
    socket.onerror = function(error) {
        alert("Ошибка " + error.message);
    };
}

//----трекинг лица
function OnServer_FaceRecognize(){
	if(str_video.length>2){
		$.ajax({
			url:"http://127.0.0.1:5001/face_detect",
			mode: 'no-cors',
			type:"POST",
			contentType:"applicattion/json",
			dataType:"json",
			data:JSON.stringify({ dates : str_video }),
			success:function(message){
				document.getElementById("r_video_block").src = "data:image/jpeg;base64," + message["message"].split("'")[1];
				if(b_OnServer_FaceRecognize) OnServer_FaceRecognize();
			}
		});
	}else{ console.log("null"); }
}
//---наличие лица
function OnServer_isFaceRecognize(){
	if(str_video.length>2){
		$.ajax({
			url:"http://127.0.0.1:5001/isface_detect",
			mode: 'no-cors',
			type:"POST",
			contentType:"applicattion/json",
			dataType:"json",
			data:JSON.stringify({ dates : str_video }),
			success:function(message){
				document.getElementById("name").innerHTML = "[ " + message["message"]+" ]";
				if(b_OnServer_isFaceRecognize) OnServer_isFaceRecognize();
			}
		});
	}else{ console.log("null"); }
}
//---наличие самого человека
function OnServer_isBodyRecognize(){
	if(str_video.length>2){
		$.ajax({
			url:"http://127.0.0.1:5001/isbody_detect",
			mode: 'no-cors',
			type:"POST",
			contentType:"applicattion/json",
			dataType:"json",
			data:JSON.stringify({ dates : str_video }),
			success:function(message){
				document.getElementById("ishave").innerHTML = "[ " + message["message"]+" ]";
				if(b_OnServer_isBodyRecognize) OnServer_isBodyRecognize();
			}
		});
	}else{ console.log("null"); }
}
//--------------------
function start_monitor() {
    /*b_OnServer_isFaceRecognize=true;
    b_OnServer_isBodyRecognize=true;
    OnServer_isFaceRecognize();
    OnServer_isBodyRecognize();*/
	if(document.getElementById('c_s').getAttribute('class')=='s_h2_g'){
		b_OnServer_isUniverce=true;
		OnServer_isUniverce();
		document.getElementById('imgBut_mn').setAttribute("onclick","stop_monitoring()");
		document.getElementById('imgBut_mn').setAttribute("value","остановить мониторинг");
	}
}
function stop_monitoring() {
    /*b_OnServer_isFaceRecognize=false;
    b_OnServer_isBodyRecognize=false;*/
    b_OnServer_isUniverce=false;
    document.getElementById('imgBut_mn').setAttribute("onclick","start_monitor()");
    document.getElementById('imgBut_mn').setAttribute("value","начать мониторинг");
	setMessage('off');
}
function tracking_face() {
    b_OnServer_FaceRecognize=true;
    OnServer_FaceRecognize();
    document.getElementById('imgBut_tr').setAttribute("onclick","dont_tracking_face()");
    document.getElementById('imgBut_tr').setAttribute("value","остановить трекинг лица");
}
function dont_tracking_face() {
    b_OnServer_FaceRecognize=false;
    document.getElementById('imgBut_tr').setAttribute("onclick","tracking_face()");
    document.getElementById('imgBut_tr').setAttribute("value","трекинг лица");
}

//----univerce
function OnServer_isUniverce(){
	if(str_video.length>2){
		$.ajax({
			url:"http://127.0.0.1:5001/isuniverce_detect",
			mode: 'no-cors',
			type:"POST",
			contentType:"applicattion/json",
			dataType:"json",
			data:JSON.stringify({
			    dates : str_video,
			    bf1 : document.getElementById('1bf').value,
			    bf2 : document.getElementById('2bf').value,
			    bf3 : document.getElementById('3bf').value,
			    bf4 : document.getElementById('4bf').value,
			    bf5 : document.getElementById('5bf').value,
			}),
			success:function(message){
			    /*if(document.getElementById('5bf').value=='-') {
				    document.getElementById("name").innerHTML = "[ " + message["message"]+" ] (подготовка к анализу)";
				} else {
				    document.getElementById("name").innerHTML = "[ " + message["message"]+" ] ("+document.getElementById('1bf').value+")";
				}*/
				mess = 'off';
				if(document.getElementById('imgBut_mn').getAttribute('value')=='остановить мониторинг') { mess=message["message"]; }
				setMessage(mess);
				reverce(message["message"]);
				if(b_OnServer_isUniverce) OnServer_isUniverce();
				if(mess=='Потеря сознания' && lastCrit==false){
					addStat();
					lastCrit=true;
				}
			}
		});
	}else{ console.log("null"); }
}
function reverce(newvalue){
    document.getElementById('5bf').setAttribute("value", document.getElementById('4bf').value);
    document.getElementById('4bf').setAttribute("value", document.getElementById('3bf').value);
    document.getElementById('3bf').setAttribute("value", document.getElementById('2bf').value);
    document.getElementById('2bf').setAttribute("value", document.getElementById('1bf').value);
    document.getElementById('1bf').setAttribute("value", newvalue);
}
function clearstate(){
    document.getElementById('5bf').setAttribute("value", '-');
    document.getElementById('4bf').setAttribute("value", '-');
    document.getElementById('3bf').setAttribute("value", '-');
    document.getElementById('2bf').setAttribute("value", '-');
    document.getElementById('1bf').setAttribute("value", '-');
}

function setMessage(msg){
	if(msg=='off'){
		document.getElementById("light_signal").setAttribute("src", 'static/light_off.png');
		document.getElementById("isHK").setAttribute("class", 's_h2');
		document.getElementById("string_out").innerHTML = 'Сотрудник : <i>(наблюдение не ведется)</i>';
	}else{
		if(document.getElementById('5bf').value=='-') {
			document.getElementById("isHK").setAttribute("class", 's_h2_y');
			document.getElementById("string_out").innerHTML = 'Сотрудник : <i>(подготовка к анализу)</i>';
			document.getElementById("light_signal").setAttribute("src", 'static/light_off.png');
		}else{
			switch (msg){ //'Лицо', 'Тело', 'Встал', 'Сел', 'Ушел', 'Отсутствует', 'Пришел', 'Пропал', 'Потеря сознания'
				case 'Потеря сознания' : {
					document.getElementById("light_signal").setAttribute("src", 'static/light_r.png');
					document.getElementById("isHK").setAttribute("class", 's_h2_r');
					document.getElementById("string_out").innerHTML = 'Сотрудник : <b>потеря сознания</b>';
					break;
				}
				case 'Пропал' : {
					document.getElementById("light_signal").setAttribute("src", 'static/light_y.png');
					document.getElementById("isHK").setAttribute("class", 's_h2_y');
					document.getElementById("string_out").innerHTML = 'Сотрудник : <b>пропал</b>';
					break;
				}
				case 'Отсутствует' : {
					document.getElementById("light_signal").setAttribute("src", 'static/light_g.png');
					document.getElementById("isHK").setAttribute("class", 's_h2_y');
					document.getElementById("string_out").innerHTML = 'Сотрудник : <b>не на рабочем месте</b>';
					break;
				}
				case 'Ушел' : {
					document.getElementById("light_signal").setAttribute("src", 'static/light_g.png');
					document.getElementById("isHK").setAttribute("class", 's_h2_y');
					document.getElementById("string_out").innerHTML = 'Сотрудник : <b>не на рабочем месте</b>';
					break;
				}
				default :{
					document.getElementById("light_signal").setAttribute("src", 'static/light_g.png');
					document.getElementById("isHK").setAttribute("class", 's_h2_g');
					document.getElementById("string_out").innerHTML = 'Сотрудник : <b>на рабочем месте</b>';
				}
			}
		}
	}
}
//--------статистика
function updateStat(str){
	$.ajax({
		url:"http://127.0.0.1:5000/statistics",
		mode: 'no-cors',
		type:"POST",
		contentType:"applicattion/json",
		dataType:"json",
		data:JSON.stringify({ sts : "crit", dates : str, l_ip : l_ip, l_pt : l_pt }),
		success:function(message){
			document.getElementById("sts").innerHTML = message["message"];
		}
	});
}
function addStat(){
	$.ajax({
		url:"http://127.0.0.1:5000/statistics",
		mode: 'no-cors',
		type:"POST",
		contentType:"applicattion/json",
		dataType:"json",
		data:JSON.stringify({ sts : "add_crit", l_ip : l_ip, l_pt : l_pt }),
		success:function(message){
			document.getElementById("sts").innerHTML = message["message"];
		}
	});
}