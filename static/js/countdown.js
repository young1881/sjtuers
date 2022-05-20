function refactor_countdown(){
    $.ajax({
        url:'/index/refactor_countdown/',
        method:'post',
        data: {
            "refactor_date_name": $("#refactor_date_name").val(),
            "year": $("#YYYY").val(),
            "month": $("#MM").val(),
            "day": $("#DD").val(),
            'csrfmiddlewaretoken': csrf_token,
        },
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