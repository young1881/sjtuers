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
    } else if (type === '中雨' || type === '大雨'){
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