/**
 * Created by JOYyuan on 16/7/8.
 */
var productList;
var num;
var pageId = 1;
var ulEle;
var phone;
var user;
var deleteId;
var editId;
$(document).ready(
    function () {
        jQuery.validator.addMethod("decimal", function (value, element) {
            return this.optional(element) || /^\d+\.?\d{0,2}$/.test(value);
        }, "小数位不能超过两位");
        $('#exitLogin').click(function () {
            sessionStorage.removeItem('phone');
            sessionStorage.removeItem('username');
            sessionStorage.removeItem('password');
        });
        $('body').hide();
        phone = sessionStorage.phone;
        user = sessionStorage.username;
        if (phone == undefined) {
            window.location.href = "login.html";
        } else {
            $('body').show();
            productListGet();
            $('#manager').html(user);
        }

        $("#createForm").validate({
            debug: false,
            rules: {
                productName: {
                    required: true,
                    maxlength: 15
                },
                buyLink: {
                    required: true,
                    url: true
                },
                lowestPrice: {
                    required: true,
                    decimal: true
                },
                accessBuy: {
                    required: true,
                    number: true
                }
            },
            messages: {
                productName: {
                    required: "请输入产品名称",
                    maxlength: "产品名不得超过15个字符"
                },
                buyLink: {
                    required: "请输入购买连接",
                    url: "请输入正确的购买连接"
                },
                lowestPrice: {
                    required: "请输入最低价",
                    decimal: "请按正确的格式输入"

                },
                accessBuy: {
                    required: "请输入可购买量",
                    number: "请输入正确的数字"
                }
            },
            submitHandler: function (form) {
                if ($("#createForm").valid()) {
                    listUpgrade();
                }
            }
        });
        $("#editForm").validate({
            debug: false,
            rules: {
                proName: {
                    required: true,
                    maxlength: 15
                },
                shopLink: {
                    required: true,
                    url: true
                },
                lowest: {
                    required: true,
                    decimal: true
                },
                access: {
                    required: true,
                    number: true
                }
            },
            messages: {
                proName: {
                    required: "请输入产品名称",
                    maxlength: "产品名不得超过15个字符"
                },
                shopLink: {
                    required: "请输入购买连接",
                    url: "请输入正确的购买连接"
                },
                lowest: {
                    required: "请输入最低价",
                    decimal: "请按正确的格式输入"

                },
                access: {
                    required: "请输入可购买量",
                    number: "请输入正确的数字"
                }
            },
            submitHandler: function (form) {
                if ($("#editForm").valid()) {
                    productEdit();
                }
            }
        });
    }
);
function listUpgrade() {
    var name = $("#productName").val();
    var pointPrice = $("#lowestPrice").val();
    var price = pointPrice * 100;
    var num = $("#accessBuy").val();
    var buyLink = $("#buyLink").val();
    var priceInt = Number(price);
    var numInt = Number(num);
    if (name.length != 0 && priceInt.length != 0 && numInt.length != 0 && buyLink.length != 0) {
        listAddSend(name, price, num, buyLink);
    } else {
        alert("请检查输入！")
    }
}
function listAddSend(productName, lowest, weight, url) {
    $.post("/api/rice",
        {
            "product_name": productName,
            "min_price": lowest,
            "avaliable_weight": weight,
            "url": url
        }, function (result) {
            var static = result.ok;
            switch (static) {
                case true:
                    alert("添加成功");
                    $("#myModal").modal("hide");
                    productListGet();
                    location.reload();
                    break;
                case false:
                    alert("抱歉！新增错误！");
            }
        });
}
function productListGet() {
    $.get("/api/rice", {
        "page": pageId,
        "page_size": 10
    }, function (result) {
        productList = result.items;
        num = result.pages;
        proListGenerate();
    });
}
function proListGenerate() {
    var t = "";
    t += '<table id="productTable">';
    t += " <tr>" +
        "<th class='productName' >品名</th>" +
        "<th class='lowestPrice'>最低价 (元/斤)</th>" +
        "<th class='available'>可购买 （吨）</th>" +
        "<th class='buyUrl'>购买连接</th>" +
        "<th class='action'>操作</th>" +
        "</tr>";
    for (var i = 0; i < productList.length; i++) {
        t += "<tr>";
        t += "<td>" + productList[i].product_name + "</td>";
        t += "<td>" + productList[i].min_price / 100 + "</td>";
        t += "<td>" + productList[i].avaliable_weight + "</td>";
        t += "<td>" + productList[i].url + "</td>";
        t += "<td>" + "<div class='actionBox'><div class='editBox'></div>&emsp;&emsp;&emsp;&emsp;<div class='delBox'></div></div>" + "</td>";
        t += "</tr>";
    }
    t += "</table>";
    $('#NowProductList').append(t);
    $('.delBox').each(function (h) {
        $(this).attr('id', 'delete' + h);
    });
    $(".editBox").each(function (p) {
        $(this).attr('id', 'edit' + p);
    });
    for (var k = 0; k < productList.length; k++) {
        var delBtn = document.createElement("button");
        var realId = productList[k].id;
        delBtn.innerHTML = "删除";
        delBtn.id = 'del' + realId;
        (function (k) {
            delBtn.addEventListener("click", function (d) {
                $('#delConfirm').off('click');
                deleteId = productList[k].id;
                $('#delModal').modal('show');
                $('#delConfirm').one('click', function () {
                    tableDelete();
                });
            }, false);
        })(k);
        $('#delete' + k).append(delBtn);

    }
    for (var a = 0; a < productList.length; a++) {
        var editBtn = document.createElement("button");
        editBtn.innerHTML = "编辑";
        editBtn.id = 'del' + productList[a].id;
        (function (a) {
            editBtn.addEventListener("click", function (d) {
                editId = productList[a].id;
                $('#editModal').modal('show');
                putInfo();
            }, false);
        })(a);
        $('#edit' + a).append(editBtn);

    }

    pageListBuild(num);

}
function pageListBuild(pages) {
    var pagesOut = "每页10条数据，共有" + pages + "页";
    ulEle = document.createElement('ul');
    $('.aPage').html(pagesOut);
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
                $('#productTable').remove();
                $(ulEle).remove();
                productListGet();
            }, false);
        })(k);
        $("#page_" + k).append(aPage);
    }
    var liId = pageId - 1;
    $("#page_" + liId).addClass("active");
}

function tableDelete() {
    $.ajax({
        url: '/api/rice/' + deleteId,
        type: 'DELETE',
        success: function () {
            $('#delModal').modal('hide');
            alert("删除成功");
            location.reload();
        }
    });
}
function productEdit() {
    var price = Number($('#lowest').val() * 100);
    var accessBuy = Number($('#access').val());
    $.ajax({
        url: '/api/rice/' + editId,
        type: 'PUT',
        data: {
            'product_name': $('#proName').val(),
            'min_price': price,
            avaliable_weight: accessBuy,
            url: $('#shopLink').val()
        },
        success: function (result) {
            var status=result.ok;
            switch (status){
                case true:
                    $('editModal').modal('hide');
                    alert("编辑成功");
                    location.reload();
                    break;
                case false:
                    alert("服务器提了一个问题");
                    break;

            }

        }
    });
}
function putInfo() {

    $.ajax({
        url: '/api/rice/' + editId,
        type: 'GET',
        success: function (result) {
            var status = result.ok;
            var editInfo = result.item;
            switch (status) {
                case true:
                    $('#proName').val(editInfo.product_name);
                    $('#lowest').val(editInfo.min_price);
                    $('#access').val(editInfo.avaliable_weight);
                    $('#shopLink').val(editInfo.url);
                    break;
                case false:
                    alert("服务器提了一个问题");
                    break;
            }
        }
    });
}
