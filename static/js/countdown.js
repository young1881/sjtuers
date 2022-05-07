function refactor_countdown(){
    $.ajax({
        url:'/index/refactor_countdown/',
        method:'post',
        data: {
            "refactor_date_name": $("#refactor_date_name").val(),
            "year": $("#YYYY").val(),
            "month": $("#MM").val(),
            "day": $("#DD").val(),
        }
    })
    location.reload();
}