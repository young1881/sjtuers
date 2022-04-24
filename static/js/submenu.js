$("#sub-menu").hide();

$(".box").on("contextmenu", function(event){undefined
    event.preventDefault();//取消默认的浏览器自带右键
    site_name = this.id;

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

function delete_site(){
    console.log("成功调用");
    $.ajax({
    url: "/index/",
    type: "POST",        //请求类型
    data: {"delete_site_name": site_name},
    dataType: "html",
    success: function () {
        delete_site_name=document.getElementById(site_name).style.display='none';
        console.log("已删除");
    },
    error: function () {
        //当请求错误之后，自动调用
    }
})}

function openRefactorDialog(){
    document.getElementById('refactor_site').style.display='block';
    var url = document.getElementById(site_name+'url').href;
    document.getElementById('refactor_site_name').value = site_name;
    document.getElementById('refactor_site_url').value = url;
}
function closeRefactorDialog(){
    document.getElementById('refactor_site').style.display='none';
}
