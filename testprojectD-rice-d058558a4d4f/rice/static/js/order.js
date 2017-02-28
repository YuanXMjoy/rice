/**
 * Created by JOYyuan on 16/7/8.
 */
var pageId = 1;
var orderList;
var phone;
var user;
var key;
$(document).ready(function () {
    $('#exitLogin').click(function () {
        sessionStorage.removeItem('phone');
        sessionStorage.removeItem('username');
        sessionStorage.removeItem('password');
    });
    $('body').hide();
    phone = sessionStorage.phone;
    user = sessionStorage.username;
    key = sessionStorage.password;
    if (phone == undefined) {
        window.location.href = "login.html";
    } else {
        $('body').show();
        orderGet();
        $('#serviceNow').html(phone);
        $('#manager').html(user);

    }
    $('#phoneForm').validate({
        debug: false,
        rules: {newServicePhone: {required: true, digits: true, maxlength: 11, minlength: 11}},
        messages: {newServicePhone: {required: "请输入电话号码", digits: "电话号码不规范", minlength: "手机号码11位"}},
        submitHandler: function (form) {
            if ($("#phoneForm").valid()) {
                phoneNum();
            }
        }
    });


});
function phoneNum() {
    var newNumber = $('#newServicePhone').val();
    if (newNumber.length != 0) {
        newPhoneSend(user, key, newNumber);
    } else {
        alert("请检查输入");
    }
}
function newPhoneSend(userName, password, phoneNumber) {
    $.ajax({
        url: '/api/change_phone',
        type: 'PUT',
        data: {
            'username': userName,
            'password': password,
            "phone_number": phoneNumber
        },
        success: function (result) {
            var static = result.ok;
            switch (static) {
                case true:
                    alert("修改手机号码成功！");
                    $("#newServicePhone").val("");
                    $("#myModal").modal("hide");
                    $("#serviceNow").html(phoneNumber);
                    break;
                case false:
                    alert('修改手机号失败');
                    break;
            }
        }
    });
}

function orderGet() {
    $.get('/api/order', {
        page: pageId,
        page_size: 10
    }, function (result) {
        orderList = result.items;
        var pages = result.pages;
        var pageCount = Number(pages);
        orderListGenerate();
        pageListBuild(pageCount);
    });
}
function orderListGenerate() {
    var t = "";
    t += '<table id="orderTable">';
    t += " <tr>" +
        "<th class='timeTh' >时间</th>" +
        "<th class='buyerNameTh'>姓名</th>" +
        "<th class='phoneTh'>电话</th>" +
        "<th class='productNameTh'>产品名</th>" +
        "<th class='amountTh'>欲购买量 (吨)</th>" +
        "<th class='buyerPriceTh'>期望价格 （元/斤）</th>" +
        "</tr>";
    for (var i = 0; i < orderList.length; i++) {
        t += "<tr>";
        t += "<td>" + orderList[i].time + "</td>";
        t += "<td>" + orderList[i].customer + "</td>";
        t += "<td>" + orderList[i].phone_number + "</td>";
        t += "<td>" + orderList[i].product_name + "</td>";
        t += "<td>" + orderList[i].amount + "</td>";
        t += "<td>" + orderList[i].will_price + "</td>";
        t += "</tr>";
    }
    t += "</table>";
    $('#orderBox').append(t);
}
function pageListBuild(pages) {
    var pagesOut = "每页10条数据，共有" + pages + "页";
    var ulEle = document.createElement('ul');
    $('.pageP').html(pagesOut);
    $(ulEle).addClass('pagination')
        .appendTo($('#pagesGroup'));
    for (var i = 0; i < pages; i++) {
        var li = document.createElement("li");
        li.id = "page_" + i;
        $("ul").append(li);
    }
    for (var k = 0; k < pages; k++) {
        var turnValue = k + 1;
        var pageValue = "" + turnValue;
        var aPage = document.createElement("a");
        aPage.innerHTML = pageValue;
        (function (k) {
            aPage.addEventListener("click", function () {
                var page = k + 1;
                pageId = Number(page);
                $('#orderTable').remove();
                $(ulEle).remove();
                orderGet();
            }, false);
        })(k);
        $("#page_" + k).append(aPage);
    }
    var liId = pageId - 1;
    $("#page_" + liId).addClass("active");
}
