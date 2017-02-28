/**
 * Created by JOYyuan on 16/7/8.
 */


var status;
$(document).ready(function () {
    jQuery.validator.addMethod("decimal", function (value, element) {
        return this.optional(element) || /^\d+\.?\d{0,2}$/.test(value);
    }, "小数位不能超过两位");
    jQuery.validator.addMethod("isGtTwo", function(value, element) {
        return this.optional(element) || value>=2;
    }, "订购量必须大于两顿");
    $("#bookForm").validate({
        debug: false,
        rules: {
            productName: {
                required: true,
                maxlength: 15
            },
            buyerPrice: {
                required: true,
                decimal: true
            },
            amount: {
                required: true,
                digits: true,
                isGtTwo:true
            },
            buyerName: {
                required: true,
                minlength: 2,
                maxlength: 15
            },
            telephone: {
                required: true,
                digits: true,
                minlength: 11,
                maxlength: 11
            }
        },
        messages: {
            productName: {
                required: "请输入产品名称",
                maxlength: "产品名不能超过15个字符"
            },
            buyerPrice: {
                required: "请输入心理价位",
                decimal: "请按正确的格式输入"
            },
            amount: {
                required: "请输入订购数量",
                digits: "订购量只能是大于的整数"
    },
            buyerName: {
                required: "请输入您的姓名",
                minlength: "姓名不得少于2个字符",
                maxlength: "姓名不得多于15个字符"
            },
            telephone: {
                required: "请输入手机号码",
                digits: "手机号码不规范",
                minlength: "请输入11位手机号码"
            }
        },
        submitHandler: function (form) {
            if ($("#bookForm").valid()) {
                bookCheck();
            }
        }
    });

});

function bookCheck() {
    var name = $("#productName").val();
    var mentalYuan = $("#buyerPrice").val();
    var mental = Number(mentalYuan * 100);
    var num = Number($("#amount").val());
    var custom = $("#buyerName").val();
    var phone = $("#telephone").val();
    if (name.length != 0 && mental.length != 0 && num.length != 0 && custom.length != 0 && phone.length != 0) {
        bookSend(name, mental, num, custom, phone);
    } else {
        alert("请检查输入！")
    }
}
function bookSend(proName, willPrice, amount, customer, tel) {
    $.post("/api/order", {
        "product_name": proName,
        "will_price": willPrice,
        "amount": amount,
        "customer": customer,
        "phone_number": tel
    }, function (result) {
        var status=result.ok;
        switch (status){
            case true:
                window.location.href = "bookDone.html";
                break;
            case false:
                alert("服务器提了一个问题");
                break;
        }
    });

}