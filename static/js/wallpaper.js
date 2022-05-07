if (wallpaper_photo_name === 'visitor.jpg' || wallpaper_css !== "") {
    $("#base_all").css("background", wallpaper_css);
} else{
    let value = 'url("' + wallpaper_photo + '")'
    $("#base_all").css("background", value);
}

function upload_img() {
    let formData = new FormData($("#upload_img_form")[0]);
    formData.append("img_upload_username", username)
    $.ajax({
        url: "/index/upload_img/", //请求路径
        type: 'POST', // 请求类型
        data: formData, // 请求数据
        dataType: "JSON", // 返回数据格式
        contentType: false, //表示不处理数据
        processData: false,
        cache: false,
        success: function (data) {
            if (data === 1) {
                location.reload();
            }else if (data === 0) {
                alert("上传失败");
            }
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function change_color_wallpaper(obj){
    var name = obj.getAttribute('id');
    var css = name_to_css(name)
    $("#base_all").css("background", css);
    $.ajax({
        url: "/index/color_wallpaper/",
        type: "POST",        //请求类型
        data: {"css": css, "color_wallpaper_username": username, 'csrfmiddlewaretoken': csrf_token,},
    })
    closeWallpaperDialog();
}

function name_to_css(name){
    if (name === "NightFade"){
        return "linear-gradient(to top, #fbc2eb 0%, #a6c1ee 100%)"
    } else if (name === "WinterNeva"){
        return "linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%)"
    } else if (name === "SunnyDay"){
        return "linear-gradient(120deg, #f6d365 0%, #fda085 100%)"
    } else if (name === "RareWind"){
        return "linear-gradient(to top, #a8edea 0%, #fed6e3 100%)"
    } else{
        return "linear-gradient(90deg, #70e1f5 0%, #ffd194 100%)"
    }
}