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
	hljs.initHighlightingOnLoad();
	//评论模块初始化
	$('.ds-add-emote').qqFace({
		id : 'ds-smilies-tooltip', 
		assign:'saytext', 
		path:'/static/img/qqface/'	//表情存放的路径
	});
}

//评论提交验证
function checksubmit(form){
	if (form.message.value == ""){
		return false;
	}
	if (form.user_id.value){//用户已经登录
		$.ajax({
			type: "POST",
			url:'/postcomment/',
			data:$(form).serialize(),
			async: false,
			error: function(request) {
                alert("Postcomment error");
            },
            success: function(callbackdata) {
            	if (callbackdata != null){
            		//console.log($('#blog_commentnums_bottom').val());
            		var currentcomments = $('#blog_commentnums_bottom').children().get(0).innerHTML;
            		var newcomments = parseInt(currentcomments)+ 1;
            		$('#blog_commentnums_bottom').children().get(0).innerHTML = newcomments;
            		$('#blog_commentnums_top').get(0).innerHTML = newcomments+'条评论';
            		if(form.parent_id){//非一级评论
            			var replybox = $(form).parent();
            			if(replybox.prev().hasClass("ds-reply-active")){
            				replybox.slideToggle(function(){
            					$(this).remove();
            				});//滑动隐藏后删除
            				replybox.prev().removeClass("ds-reply-active");
            			}
            			var parentcomment = $('#comments_id_'+form.parent_id.value);
            			if (parentcomment.next().length){//已有子评论
            				$(callbackdata).appendTo(parentcomment.next());
            			} else {//没有子评论
            				var htmldata = '<ul class="ds-children">'+callbackdata+'</ul>';
            				$(htmldata).appendTo(parentcomment.parent());
            			}
            		} else {//一级评论
            			var commentul = $('#ds-reset').children('ul.ds-comments');
            			if(commentul.children().first().hasClass("ds-post-placeholder")) {
            				commentul.children().first().remove();
            			}
            			$(callbackdata).appendTo(commentul);
            		}
            		return false;
            	}
            }
		});
		form.reset();//清空表单
		return false;//用户已登录
	} else {
		$("#loginmodel").modal('show');
	}
	return false;
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
//检查登录
function checklogin(form){
	if (form.email.value == "" || form.password.value == ""){
		showregistermsg($(form.email),"has-error","用户名或密码不能为空!");
		showregistermsg($(form.password),"has-error","用户名或密码不能为空!");
		return false;
	}
	$.ajax({
		type: "POST",
		url:'/account/login/',
		data:$(form).serialize(),
		async: false,
		error: function(request) {
            alert("Connection error");
        },
        success: function(callbackdata) {
        	if (callbackdata == '1'){
        		showregistermsg($(form.email),"has-error","请输入邮箱和密码!");
        		return true;
        	} else if (callbackdata == '2'){
        		showregistermsg($(form.email),"has-error","无效的邮箱,请重新输入!");
        		return true;
        	} else if (callbackdata == '3'){
        		showregistermsg($(form.password),"has-error","密码错误!");
        		return true;
        	} else {
        		$("#loginmodel").modal('hide');
        		$('#loginarea').nextAll().remove();
        		$(callbackdata).appendTo($('#loginarea').parent());
        		$('.ds-add-emote').qqFace({
        			id : 'ds-smilies-tooltip', 
        			assign:'saytext', 
        			path:'/static/img/qqface/'	//表情存放的路径
        		});
        		//location.reload();
    		return true;
        	}
        }
	});
	form.reset();//清空表单
	return false;
}
function checklogout(form){
	$.ajax({
		type: "POST",
		url:'/account/logout/',
		data:$(form).serialize(),
		async: false,
		error: function(request) {
            alert("Connection error");
        },
        success: function(callbackdata) {
        	if (callbackdata == 'logoutfail'){
        		alert('注销失败!')
        		return true;
        	} else {
        		$('#loginarea').nextAll().remove();
        		$(callbackdata).appendTo($('#loginarea').parent());
        		$('.ds-add-emote').qqFace({
        			id : 'ds-smilies-tooltip', 
        			assign:'saytext', 
        			path:'/static/img/qqface/'	//表情存放的路径
        		});
//        		QC.Login({
//        			  btnId : "qqLoginBtn",//插入按钮的html标签id
//        			  size : "C_S",//按钮尺寸
//        			  scope : "get_user_info",//展示授权，全部可用授权可填 all
//        			  display : "pc"//应用场景，可选
//        			 });
        		//location.reload();
        		return true;
        	}
        }
	});
	return false;
}

//检查注册信息
function showregistermsg(objself,classname,msginfo){
	if (!objself.parent().parent().hasClass(classname)) {
		if (classname == 'has-error'){
			var msg='<span class="glyphicon glyphicon-remove form-control-feedback"></span>';
			msg += '<label class="control-label" for="inputEmail">'+msginfo+'</label>';
		} else if (classname == 'has-success'){
			var msg='<span class="glyphicon glyphicon-ok form-control-feedback"></span>';
		} else {
			var msg = '';
		}
		objself.after(msg);
		objself.parent().parent().addClass(classname);
	}
}
function checkregistererrormsg(inputobj){
	$(inputobj).nextAll().remove();
	if ($(inputobj).parent().parent().hasClass("has-error")){
		$(inputobj).parent().parent().removeClass("has-error");
	} 
	if ($(inputobj).parent().parent().hasClass("has-success")){
		$(inputobj).parent().parent().removeClass("has-success");
	} 
}
function checkregister(form){//提交注册表单之前验证
	if (form.registeremail.value == ""){
		showregistermsg($(form.registeremail),"has-error","邮箱不能为空!");
		return false;
	}
	if (form.registerpassword.value == ""){
		showregistermsg($(form.registerpassword),"has-error","密码不能为空!");
		return false;
	}
	if (form.registerpassword.value != form.registerpassword2.value){
		showregistermsg($(form.registerpassword),"has-error","两次输入的密码不一致!");
		return false;
	}
	if (form.registernickname.value == ""){
		showregistermsg($(form.registernickname),"has-error","昵称不能为空!");
		return false;
	}
	if(form.captcha_1.value == ""){
		showregistermsg($(form.captcha_1),"has-error","未输入验证码!");
		return false;
	} else {
		//console.log($('#verifycodearea').parent().parent().serialize());
		var captcha_0 = $('#verifycodearea').children('#id_captcha_0').val();
		var captcha_1 = $('#verifycodearea').children('#id_captcha_1').val();
		$.ajax({
			type: "POST",
			url:'/account/verifycode/',
			data:'captcha_0='+captcha_0+'&captcha_1='+captcha_1,
			async: false,
			error: function(request) {
                alert("Connection error");
            },
            success: function(callbackdata) {
            	if (callbackdata == 'invalid'){
            		refreshverifycode();
            		showregistermsg($('#verifycodearea').children('#id_captcha_1'),"has-error","验证码错误!");
            		return false;
            	} else if (callbackdata == 'valid'){
            		//form.submit();
            		$.ajax({
            			type: "POST",
            			url:'/account/register/',
            			data:$(form).serialize(),
            			async: false,
            			error: function(request) {
                            alert("Connection error");
                        },
                        success: function(callbackdata) {
                        	if (callbackdata == '1'){
                        		showregistermsg($(form.registeremail),"has-error","请输入邮箱和密码!");
                        		return true;
                        	} else if (callbackdata == '2'){
                        		showregistermsg($(form.registeremail),"has-error","该邮箱已经被使用，请重新输入!");
                        		return true;
                        	} else if (callbackdata == '3'){
                        		showregistermsg($(form.registernickname),"has-error","用户名不能为空!");
                        		return true;
                        	} else {
                        		$("#registermodel").modal('hide');
                        		$('#loginarea').nextAll().remove();
                        		$(callbackdata).appendTo($('#loginarea').parent());
                        		$('.ds-add-emote').qqFace({
                        			id : 'ds-smilies-tooltip', 
                        			assign:'saytext', 
                        			path:'/static/img/qqface/'	//表情存放的路径
                        		});
                        		form.reset();//清空表单
                        		return true;
                        	}
                        }
            		});
            		
            	}
                //console.log(callbackdata);
            }
		});
	}
	return false;
}
function checkemailvalid(inputobj){
	if (inputobj.value){
		$.post('/account/verifyemail/',{email:inputobj.value},function(callbackdata){
			if (callbackdata == 'True') {
				showregistermsg($(inputobj),"has-success","");
				//alert("true");
			} else if (callbackdata == 'False'){
				showregistermsg($(inputobj),"has-error","邮箱已存在!");
				//alert("False");
			} else {
				showregistermsg($(inputobj),"has-error","请填入邮箱!");
				//alert("Empty");
			}
		});
	}
}
function checkpasswordvalid(inputobj){
	if (inputobj.value){
		var prevInputobj = $(inputobj).parent().parent().prev().find("#inputregisterPassword");//前一次输入的密码
		if(inputobj.value != prevInputobj.val()){
			showregistermsg($(inputobj),"has-error","两次密码不一致!");
			//alert("两次输入不一致");
		} else {
			showregistermsg($(inputobj),"has-success","");
			showregistermsg(prevInputobj,"has-success","");
		}
	}
}
function checknicknamevalid(inputobj){
	if (inputobj.value){
		showregistermsg($(inputobj),"has-success","");
	}
}

function showregistermodel() {
	$("#loginmodel").modal('hide');
	$("#registermodel").modal('show');
}

function refreshverifycode() {
	var verifycol = $("#verifycodearea");
	$.ajax({
		type: "GET",
		url: '/account/verifycode/',
		async: false,
		success: function(callbackdata) {
			verifycol.html(callbackdata);//callback为html对象
			$(verifycol).children("#id_captcha_1").addClass("form-control");
		}
	});
}