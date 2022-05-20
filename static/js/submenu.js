$("#sub-menu").hide();
var csrf_token = $("[name='csrfmiddlewaretoken']").val();
$(".box").on("contextmenu", function(event){undefined
    event.preventDefault();//取消默认的浏览器自带右键
    site_name = this.id;
    site_url = this.getAttribute("name");
    $("#sub-menu").show(100)
    $('#sub-menu').css({
        'top': event.pageY + 'px',
        'left': event.pageX + 'px'
    });
})

$(document).on('click', function(event) {
    var evt = event.srcElement ? event.srcElement : event.target;
    if (evt.id == 'sub-menu') {
        return;
    } else {
        $('#sub-menu').hide();
    }
});

function add_site() {
    $.ajax({
        url:'/index/add_site/',
        method:'post',
        data:{"site_name":$("#site_name").val(),
            "site_url":$("#site_url").val(),
            'csrfmiddlewaretoken': csrf_token,
        },
        dataType: "JSON",
        success: function (response) {
            if (response === 1) {
                window.open('/index/','_self');
            }else if (response === 0) {
                alert("超出添加上限，请删除不需要的网址后再添加！");
            } else if (response === 2){
                alert("该网址已存在，已将其重命名！")
            } else if (response === 3){
                alert("没有检测到您的输入！")
            }
        },
        error: function () {
            alert("请求失败，请联系管理员！")
        }
    })
}

function refactor_site(){
    $.ajax({
        url:'/index/refactor_site/',
        method:'post',
        data:{"refactor_site_name":$("#refactor_site_name").val(),
            "refactor_site_url": site_url,
            'csrfmiddlewaretoken': csrf_token,
        },
        dataType: "JSON",
        success: function (response) {
            if (response === 1) {
                window.open('/index/','_self');
            }else if (response === 0) {
                alert("没有检测到您的输入！")
            }
        },
        error: function () {
            alert("请求失败，请联系管理员！")
        }
    })
}

function delete_site(){
    $.ajax({
        url: "/index/delete_site/",
        type: "POST",        //请求类型
        data: {"delete_site_name": site_name,'csrfmiddlewaretoken': csrf_token,},
        dataType: "html",
        success: function (response) {
            delete_site_name=document.getElementById(site_name).style.display='none';
        },
        error: function () {
            alert("请求失败，请联系管理员！")
        }
})}

function openRefactorDialog(){
    document.getElementById('refactor_site').style.display='block';
}
function closeRefactorDialog(){
    document.getElementById('refactor_site').style.display='none';
}
