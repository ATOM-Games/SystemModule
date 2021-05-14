function clearReport(ip, pt){
	$.ajax({
		url:"http://"+ip+":"+pt+"/clear",
		mode: 'no-cors',
		type:"POST",
		contentType:"applicattion/json",
		dataType:"json",
		data:JSON.stringify({ clear : "clear" }),
		success:function(message){
			if(message["message"]=='good'){
				location.href=location.href;
			}else{
				location.href=location.href;
			}
		}
	});
}