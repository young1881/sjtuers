var type = [];
var icon = [];
for (var i=0; i<=3; i++){
    var type_id = 'day' + i + '_type';
    var icon_id = 'day' + i + '_icon';
    type[i] = document.getElementById(type_id).innerText;
    icon[i] = document.getElementById(icon_id);
    var class_content = type_to_icon(type[i]);
    icon[i].className = class_content;
}
function type_to_icon(type){
    if (type === '晴'){
        return 'wi wi-day-sunny';
    } else if (type === '多云'){
        return 'wi wi-day-cloudy';
    } else if (type === '阴'){
        return 'wi wi-cloudy';
    } else if (type === '小雨'){
        return 'wi wi-sprinkle';
    } else if (type === '阵雨'){
        return 'wi wi-showers';
    } else if (type === '中雨' || type === '大雨' || type === '暴雨'){
        return 'wi wi-rain';
    } else if (type === '雷阵雨'){
        return 'wi wi-storm-showers';
    } else if (type === '雾'){
        return 'wi wi-fog';
    } else if (type === '沙尘暴') {
        return 'wi wi-sandstorm';
    } else if (type === '雪' || type === '小雪' || type === '中雪' || type === '大雪'){
        return 'wi wi-snow';
    } else {
        return 'wi wi-refresh';
    }
}

document.getElementById("forecast").firstElementChild.firstElementChild.remove();

$('[data-role="cityselector"]').citySelector({ callback: function (item, index) { } });

$('#getVal').click(function () {
    var currentVal = document.getElementById('cityselect').innerHTML;
    var currentArr = currentVal.split(' ');
    if (typeof (currentArr[2]) !== "undefined")
        var currentCity = currentArr[2];
    else if (typeof (currentArr[1]) !== "undefined")
        var currentCity = currentArr[1];
    else alert("请选择查询天气的城市！");
    if (typeof (currentCity) !== "undefined") {
        update_weather();
    }

    function update_weather () {
        if (window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
        }
        else {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        url = 'http://wthrcdn.etouch.cn/WeatherApi?city=' + currentCity;
        xmlhttp.open("GET", url, false);
        xmlhttp.send();
        xmlDoc = xmlhttp.responseXML;
        console.log(xmlDoc.getElementsByTagName("resp"));
        if (xmlDoc.getElementsByTagName("resp")[0].childNodes[0].childNodes[0].nodeValue === "invalid city") {
            alert("所选城市不存在或已撤销");
        }
        else {
            document.getElementById("currentcity").innerText = currentCity;
            document.getElementById("day0_type").innerText = xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[0].childNodes[3].childNodes[0].childNodes[0].nodeValue;
            document.getElementById("day0_icon").className = type_to_icon(xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[0].childNodes[3].childNodes[0].childNodes[0].nodeValue);
            document.getElementById("day0_temp").innerHTML = "当前 " + xmlDoc.getElementsByTagName("resp")[0].childNodes[2].childNodes[0].nodeValue + "℃<br>今日 " + xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[0].childNodes[2].childNodes[0].nodeValue.replace(/[^\d]/g, "") + "~" + xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[0].childNodes[1].childNodes[0].nodeValue.replace(/[^\d]/g, "") + "℃";
            document.getElementById("day1_type").innerText = xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[1].childNodes[3].childNodes[0].childNodes[0].nodeValue;
            document.getElementById("day1_icon").className = type_to_icon(xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[1].childNodes[3].childNodes[0].childNodes[0].nodeValue);
            document.getElementById("day1_temp").innerHTML = xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[1].childNodes[2].childNodes[0].nodeValue.replace(/[^\d]/g, "") + "/" + xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[1].childNodes[1].childNodes[0].nodeValue.replace(/[^\d]/g, "");
            document.getElementById("day2_type").innerText = xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[2].childNodes[3].childNodes[0].childNodes[0].nodeValue;
            document.getElementById("day2_icon").className = type_to_icon(xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[2].childNodes[3].childNodes[0].childNodes[0].nodeValue);
            document.getElementById("day2_temp").innerHTML = xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[2].childNodes[2].childNodes[0].nodeValue.replace(/[^\d]/g, "") + "/" + xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[2].childNodes[1].childNodes[0].nodeValue.replace(/[^\d]/g, "");
            document.getElementById("day3_type").innerText = xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[3].childNodes[3].childNodes[0].childNodes[0].nodeValue;
            document.getElementById("day3_icon").className = type_to_icon(xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[3].childNodes[3].childNodes[0].childNodes[0].nodeValue);
            document.getElementById("day3_temp").innerHTML = xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[3].childNodes[2].childNodes[0].nodeValue.replace(/[^\d]/g, "") + "/" + xmlDoc.getElementsByTagName("resp")[0].childNodes[11].childNodes[3].childNodes[1].childNodes[0].nodeValue.replace(/[^\d]/g, "");
        }
    }
    
    document.getElementById('citywindow').style.display = "none";
    document.getElementById('currentcity').style.display = "inline";
    document.getElementById('edit').style.display = "inline-block";
});

$('#edit').click(function () {
    document.getElementById('citywindow').style.display = "block";
    document.getElementById('currentcity').style.display = "none";
    this.style.display = "none";
});

$('#currentcity, #day0_icon, li, .type, .T_current').click(function () {
    window.open("/weather/", "_blank");
});