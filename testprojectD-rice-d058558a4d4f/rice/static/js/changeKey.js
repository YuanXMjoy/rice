/**
 * Created by JOYyuan on 16/7/8.
 */
var userName;
$(document).ready(
    function () {
        $('#exitLogin').click(function () {
            sessionStorage.removeItem('phone');
            sessionStorage.removeItem('username');
            sessionStorage.removeItem('password');
        });
        $('body').hide();
        userName = sessionStorage.username;
        if (userName == undefined) {
            window.location.href = "login.html";
        } else {
            $('body').show();
            $('#manager').html(userName);

        }
        $('#passForm').validate({
            debug: false,
            rules: {
                lastKey: {
                    required: true,
                    maxlength: 18
                },
                newKey: {
                    required: true,
                    maxlength: 18
                },
                newKeyAgain: {
                    required: true,
                    equalTo: "#KeyAgain",
                    maxlength: 18
                }
            },
            messages: {
                lastKey: {
                    required: "请输入旧密码",
                    maxlength: "不能超过18位"
                },
                newKey: {
                    required: "请输入新密码",
                    maxlength: "不能超过18位"
                },
                newKeyAgain: {
                    required: "请再次输入新密码",
                    equalTo: "两次密码不相符",
                    maxlength: "不能超过18位"


                }
            },
            submitHandler: function (form) {
                if ($("#passForm").valid()) {
                    keyChange();
                }
            }
        })
        ;

    }
)
;
function keyChange() {
    var last = $('#lastKey').val();
    var newWord = $('#newKey').val();
    var newAgain = $('#newKeyAgain').val();
    if (name.length && last.length != 0 && newWord.length != 0 && newAgain.length != 0) {
        changeSend(name, last, newWord);
    } else {
        alert("请检查输入！")
    }
}
function changeSend(user, old, newKey) {
    $.ajax({
        url: '/api/change_password',
        type: 'PUT',
        data: {
            'username': user,
            'old_password': old,
            'new_password': newKey
        },
        success: function (result) {
            var static = result.ok;
            switch (static) {
                case true:
                    $('#myModal').modal('show');
                    break;
                case false:
                    alert('修改密码失败');
                    break;
            }

        }
    });

}