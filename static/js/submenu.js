$("#sub-menu").hide();

$(".box").on("contextmenu", function(event){undefined
    event.preventDefault();//取消默认的浏览器自带右键
    var delete_site_name = this.id;
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
    $.ajax({
    url: "/index/",
    type: "POST",        //请求类型
    data: {"delete_site_name": delete_site_name},
    dataType: "json",
    success: function (callback) {
        //当请求执行完成后，自动调用
        //callback, 服务器返回的数据
        console.log(callback);
    },
    error: function () {
        //当请求错误之后，自动调用
    }
})}
