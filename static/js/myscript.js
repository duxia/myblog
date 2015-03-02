function init(){
	ZeroClipboard.config({
  		hoverClass: "btn-clipboard-hover"
	});
	var client = new ZeroClipboard( $(".btn-clipboard") );
	
	client.on("ready",function(readyEvent){
		//alert("ZeroClipboard SWF is ready!");
		
		globalenv = $("#global-zeroclipboard-html-bridge");
		globalenv.data("placement", "top").attr("title", "复制到剪贴板").tooltip()//设置工具栏提示框
		//console.log(globalenv.data("placement", "top"));
		//copy响应
		client.on("copy",function(event){
			//console.log(event);
			//var c = $(this).parent();//.nextAll("pre").first();
			//console.log($(event.target).parent().nextAll("pre").first().text());
			var text = $(event.target).parent().next("pre").text();
			//console.log(c);
			//console.log(this);//this指向当前的zeroclip对象
			//console.log($(this));
			event.clipboardData.setData("text/plain", text);
			//this.setText(text);均可
		});
		//copy完成后响应
		client.on("aftercopy", function() {
            globalenv.attr("title", "复制完成!").tooltip("fixTitle").tooltip("show").attr("title", "复制到剪贴板").tooltip("fixTitle");
        });
        //加载出错
        client.on("error",function() {
        	globalenv.attr("title", "您的浏览器需要安装 Flash 插件").tooltip("fixTitle").tooltip("show");
        });
	});
}

function getCookie(cookieName) {
    var strCookie = document.cookie;
    var arrCookie = strCookie.split("; ");
    for(var i = 0; i < arrCookie.length; i++){
        var arr = arrCookie[i].split("=");
        if(cookieName == arr[0]){
            return arr[1];
        }
    }
    return "";
}

function checksubmit(form){
	if (form.message.value == ""){
		return false;
	}
	var username = getCookie("username");
	if (username){
		return true;//用户已登录
	} else {
		alert("请先登录!");
	}
	return false;
}

function checklogin(form){
	if (form.email.value == "" || form.password.value == ""){
		alert("用户名或密码不能为空!");
		return false;
	}
	return true;
}

function checkregister(form){
	if (form.registeremail.value == ""){
		alert("邮箱不能为空!");
		return false;
	}
	if (form.registerpassword.value == ""){
		alert("密码不能为空!");
		return false;
	}
	if (form.registernickname.value == ""){
		alert("昵称不能为空!");
		return false;
	}
	return true; 
}

function showregistermodel() {
	$("#loginmodel").modal('hide');
	$("#registermodel").modal('show');
}