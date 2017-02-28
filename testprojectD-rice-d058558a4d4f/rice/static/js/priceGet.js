/**
 * Created by JOYyuan on 16/7/5.
 */
var priceList;
var list;
var pageId = 1;
var num;

$(document).ready(
    function () {
        listGet();
    }
);
function listGet() {
    $.get(
        "/api/rice", {
            page: pageId,
            page_size: 10
        }, function (result) {
            priceList = result.items;
            num = result.pages;
            listGenerate();
        }
    );
}
function listGenerate() {
    var t = "";
    t += '<table id="riceTable">';
    t += " <tr>" +
        "<th class='nameTh' >品名</th>" +
        "<th class='lowestTh'>最低价 （元/斤）</th>" +
        "<th class='accessBuyTh'>可购买（吨）</th>" +
        "<th class='buyTh'>购买</th>" +
        "</tr>";
    for (var i = 0; i < priceList.length; i++) {
        t += "<tr>";
        t += "<td>" + priceList[i].product_name + "</td>";
        t += "<td>" + priceList[i].min_price/100 + "</td>";
        t += "<td>" + priceList[i].avaliable_weight + "</td>";
        t += "<td>" + "<div class='buyBox'></div>" + "</td>";
        t += "</tr>";
    }
    t += "</table>";
    $('#tableBox').append(t);
    $(".buyBox").each(function (p) {
        $(this).attr('id', 'buyBox' + p)

    });
    for(var a=0;a<priceList.length;a++){
        var aToBuy = document.createElement("a");
        aToBuy.innerHTML ="点击购买";
        aToBuy.href=priceList[a].url;
        $("#buyBox"+a).append(aToBuy);
    }
    pageListBuild(num);

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
                $('#riceTable').remove();
                $(ulEle).remove();
                listGet();
            }, false);
        })(k);
        $("#page_" + k).append(aPage);
    }
    var liId = pageId - 1;
    $("#page_" + liId).addClass("active");

}
