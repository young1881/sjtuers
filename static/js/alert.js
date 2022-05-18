function get_cookie(Name) {
    var search = Name + "=";
    var returnvalue = "";
    if (document.cookie.length > 0) {
        offset = document.cookie.indexOf(search);
        if (offset != -1) {
            // if cookie exists
            offset += search.length;
            // set index of beginning of value
            end = document.cookie.indexOf(";", offset);
            // set index of end of cookie value
            if (end == -1)
                end = document.cookie.length;
            returnvalue=decodeURI(document.cookie.substring(offset, end))
        }
    }
    return returnvalue;
}

window.alert = alert;
function alert(data) {
    var alert_box = document.createElement("div"),
        alert_p = document.createElement("p"),
        alert_h1 = document.createElement("h1")
        alert_btn = document.createElement("div"),
        textNode = document.createTextNode(data ? data : ""),
        btnText = document.createTextNode("确定"),
        h1Text = document.createTextNode("温馨提示");
    // 控制样式
    css(alert_box, {
        "position" : "fixed",
        "left" : "0",
        "right" : "0",
        "top" : "10%",
        "width" : "600px",
        "height" : "130px",
        "z-index" : "9000",
        "margin" : "0 auto",
        "background-color" : "rgba(0, 0, 0, 0.75)",
        "border-radius": "20px",
        "font-size" : "16px",
        "color" : "#fff",

    });

    css(alert_h1, {
        "text-align" : "center",
        "margin" : "15px 15px",
        "font-size" : "20px",
    })

    css(alert_p, {
        "text-align" : "center",
        "margin" : "10px 15px",
    })

    css(alert_btn, {
        "margin" : "0 auto",
        "margin-top" : "15px",
        "width" : "100px",
        "height" : "23px",
        "color" : "#000",
        "background" : "#DDD",
        "font-size" : "16px",
        "text-align" : "center",
        "border-radius": "20px",
    })
    // 内部结构套入
    alert_h1.appendChild(h1Text);
    alert_p.appendChild(textNode);
    alert_btn.appendChild(btnText);
    alert_box.appendChild(alert_h1);
    alert_box.appendChild(alert_p);
    alert_box.appendChild(alert_btn);
    // 整体显示到页面内
    document.getElementsByTagName("body")[0].appendChild(alert_box);

    // 确定绑定点击事件删除标签
    alert_btn.onclick = function() {
        alert_box.parentNode.removeChild(alert_box);
    }
}
function css(targetObj, cssObj) {
    var str = targetObj.getAttribute("style") ? targetObj.getAttribute("style") : "";
    for(var i in cssObj) {
        str += i + ":" + cssObj[i] + ";";
    }
    targetObj.style.cssText = str;
}