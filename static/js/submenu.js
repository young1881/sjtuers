$("#sub-menu").hide();

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
    console.log("成功调用");
    $.ajax({
        url:'/index/add_site/',
        method:'post',
        data:{"site_name":$("#site_name").val(),
            "site_url":$("#site_url").val()},
    })
    location.reload();
}

function refactor_site(){
    console.log(site_url)
    $.ajax({
        url:'/index/refactor_site/',
        method:'post',
        data:{"refactor_site_name":$("#refactor_site_name").val(),
            "refactor_site_url": site_url},
    })
    location.reload();
}

function delete_site(){
    delete_site_name=document.getElementById(site_name).style.display='none';
    $.ajax({
    url: "/index/delete_site/",
    type: "POST",        //请求类型
    data: {"delete_site_name": site_name},
    dataType: "html",
    success: function (response) {
        // console.log("已删除");
        console.log(response);
    },
    error: function () {
        //当请求错误之后，自动调用
    }
})}

function openRefactorDialog(){
    document.getElementById('refactor_site').style.display='block';
}
function closeRefactorDialog(){
    document.getElementById('refactor_site').style.display='none';
}
