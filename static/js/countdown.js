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
        contentType: false,
        processData: false,
        cache: false,
        success: function (response) {
            console.log(response);
            location.reload();
        },
        error: function () {
            alert("请求失败，请联系管理员！")
        }
    })
    location.reload();
}