var socket = null
var b_OnServer_FaceRecognize = false;
var b_OnServer_isFaceRecognize = false;
var b_OnServer_isBodyRecognize = false;
var b_OnServer_isUniverce = false;
var str_video="";

var l_ip="", l_pt="";
var lastCrit=false;
var lastOnWork=false;
//------настройки
var fix_crit=true;
var fix_onwork=false;
var fix_time=1;

function messageSocket(cls, msg){
	document.getElementById('c_s').innerHTML = msg;
	document.getElementById('c_s').setAttribute('class', cls);
}

function createSocket(ip, pt){
	lastCrit=false;
	lastOnWork=false;
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
		setTimeout(NewReverce, fix_time);
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
				//--потеря сознания
				if(fix_crit==true && mess=='Потеря сознания'){
					if(lastCrit==false){
						addStat('Потеря сознания');
						lastCrit=true;
					}
				}else{lastCrit=false;}
				//--потеря сознания
				if(fix_onwork==true && isWork()==true){
					if(lastOnWork==false){
						addStat('Не на рабочем месте');
						lastOnWork=true;
					}
				}else{lastOnWork=false;}
			}
		});
	}else{ console.log("null"); }
}
function NewReverce(){
	document.getElementById('5bf').setAttribute("value", document.getElementById('4bf').value);
    document.getElementById('4bf').setAttribute("value", document.getElementById('3bf').value);
    document.getElementById('3bf').setAttribute("value", document.getElementById('2bf').value);
    document.getElementById('2bf').setAttribute("value", document.getElementById('1bf').value);
	if(b_OnServer_isUniverce)setTimeout(NewReverce, fix_time);
}

function reverce(newvalue){
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
		document.getElementById("string_out").innerHTML = 'Диспетчер : <i>(наблюдение не ведется)</i>';
	}else{
		if(document.getElementById('5bf').value=='-') {
			document.getElementById("isHK").setAttribute("class", 's_h2_y');
			document.getElementById("string_out").innerHTML = 'Диспетчер : <i>(подготовка к анализу)</i>';
			document.getElementById("light_signal").setAttribute("src", 'static/light_off.png');
		}else{
			switch (msg){ //'Лицо', 'Тело', 'Встал', 'Сел', 'Ушел', 'Отсутствует', 'Пришел', 'Пропал', 'Потеря сознания'
				case 'Потеря сознания' : {
					document.getElementById("light_signal").setAttribute("src", 'static/light_r.png');
					document.getElementById("isHK").setAttribute("class", 's_h2_r');
					document.getElementById("string_out").innerHTML = 'Диспетчер : <b>потеря сознания</b>';
					break;
				}
				case 'Пропал' : {
					document.getElementById("light_signal").setAttribute("src", 'static/light_y.png');
					document.getElementById("isHK").setAttribute("class", 's_h2_y');
					document.getElementById("string_out").innerHTML = 'Диспетчер : <b>пропал</b>';
					break;
				}
				case 'Отсутствует' : {
					document.getElementById("light_signal").setAttribute("src", 'static/light_g.png');
					document.getElementById("isHK").setAttribute("class", 's_h2_y');
					document.getElementById("string_out").innerHTML = 'Диспетчер : <b>не на рабочем месте</b>';
					break;
				}
				case 'Ушел' : {
					document.getElementById("light_signal").setAttribute("src", 'static/light_g.png');
					document.getElementById("isHK").setAttribute("class", 's_h2_y');
					document.getElementById("string_out").innerHTML = 'Диспетчер : <b>не на рабочем месте</b>';
					break;
				}
				default :{
					document.getElementById("light_signal").setAttribute("src", 'static/light_g.png');
					document.getElementById("isHK").setAttribute("class", 's_h2_g');
					document.getElementById("string_out").innerHTML = 'Диспетчер : <b>на рабочем месте</b>';
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
function addStat(sit){
	$.ajax({
		url:"http://127.0.0.1:5000/statistics",
		mode: 'no-cors',
		type:"POST",
		contentType:"applicattion/json",
		dataType:"json",
		data:JSON.stringify({ sts : "add_crit", l_ip : l_ip, l_pt : l_pt, Situation : sit }),
		success:function(message){
			document.getElementById("sts").innerHTML = message["message"];
		}
	});
	sendToListener();
}
var ip_sel_list = '127.0.0.1';
var pt_sel_list = '5003';
var sendToList = false;
function sendToListener(){
	var d=new Date();
	var day=d.getDate();
	var month=d.getMonth() + 1;
	var year=d.getFullYear();
	var hour = checkTime(d.getHours());
	var min = checkTime(d.getMinutes());
	$.ajax({
		url:"http://"+ip_sel_list+":"+pt_sel_list+"/poct",
		mode: 'no-cors',
		type:"POST",
		contentType:"applicattion/json",
		dataType:"json",
		data:JSON.stringify({ dates : day+"."+month+"."+year, times : hour+":"+min, user : l_ip+":"+l_pt, mess : "Признак потери сознания" }),
		success:function(message){
			if(message["message"]=='good'){
				console.log('Слушатель принял что-то');
			}else{
				console.log('Слушатель не принял что-то');
			}
		}
	});
}
function checkTime(i)
{
	if (i<10) { i="0" + i; }
	return i;
}
function DisplayPanel(cam_lis){
	if(cam_lis=="cam"){
		document.getElementById('List_Listeners').setAttribute('style','display:none');
		document.getElementById('Sittings').setAttribute('style','display:none');
		document.getElementById('List_Cameras').setAttribute('style','display:block');
	}
	if(cam_lis=="list"){
		document.getElementById('List_Cameras').setAttribute('style','display:none');
		document.getElementById('Sittings').setAttribute('style','display:none');
		document.getElementById('List_Listeners').setAttribute('style','display:block');
	}
	if(cam_lis=="nas"){
		document.getElementById('List_Cameras').setAttribute('style','display:none');
		document.getElementById('List_Listeners').setAttribute('style','display:none');
		document.getElementById('Sittings').setAttribute('style','display:block');
	}
}

function isWork(){
	return ((document.getElementById('1bf').getAttribute("value") == 'Ушел' || document.getElementById('1bf').getAttribute("value") == 'Отсутствует') &&
		(document.getElementById('2bf').getAttribute("value") == 'Ушел' || document.getElementById('2bf').getAttribute("value") == 'Отсутствует') &&
		(document.getElementById('3bf').getAttribute("value") == 'Ушел' || document.getElementById('3bf').getAttribute("value") == 'Отсутствует') &&
		(document.getElementById('4bf').getAttribute("value") == 'Ушел' || document.getElementById('4bf').getAttribute("value") == 'Отсутствует') &&
		(document.getElementById('5bf').getAttribute("value") == 'Ушел' || document.getElementById('5bf').getAttribute("value") == 'Отсутствует'));
}
function SaveSittings(){
	fix_onwork = document.getElementById('ch1').checked;
	fix_crit = document.getElementById('ch2').checked;
	fix_time = parseInt(document.getElementById('ch3').value, 10)*200; 
}
SaveSittings();