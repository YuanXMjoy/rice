/**
 * Created by JOYyuan on 16/7/8.
 */
$(document).ready(
    function () {

        $("#loginForm").validate({
            debug:false,
            rules: {
                username: {
                    required: true,
                    minlength:2,
                    maxlength:30
                },
                password: {
                    required:true,
                    minlength:2,
                    maxlength:18
                }
            },
            messages:{
                username:{
                    required:"请输入用户名",
                    minlength:"姓名长度太短",
                    maxlength:"姓名长度太长"
                },
                password:{
                    required:"请输入密码",
                    minlength:"密码不得少于3位",
                    maxlength:"密码不得超过18位"
                }

            },
            submitHandler:function(form){
                if($("#loginForm").valid()){
                    loginCheck();
                }
            }

        });



    }

);
function loginCheck() {
            var user = $('#username').val();
            var word = $('#password').val();
            if (user.length == 0) {
                alert("请检查用户名输入");
            } else {
                if (word.length == 0) {
                    alert("请检查密码输入");
                }
                else {
                    tokenSend(user, word);
                }
            }


}
function tokenSend(name, key) {
    $.post("/api/login", {
            "username": name,
            "password": key
        }, function (result) {
            var static = result.ok;
            var phone=result.phone_number;
            sessionStorage.phone=phone;
            sessionStorage.username=name;
            sessionStorage.password=key;
            switch (static) {
                case true:
                    window.location.href = "order.html";
                    break;
                case false:
                    alert("用户名或密码错误！");
                    break;
            }

        }
    );
}
