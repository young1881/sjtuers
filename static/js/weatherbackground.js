function change_background() {
    var d = new Date();
    var hour = d.getHours();
    var body = document.getElementById("body");
    var currentVal = document.getElementById('currentWeather').innerHTML;
    var weather = currentVal.split(' ')[1];
    var time = 1;
    if (hour < 6 || hour > 17) time = 0;

    if (time && weather === '晴')
        body.style.backgroundImage = 'url(../static/img/weather_background/day_sunny.jpg)';
    else if (!time && weather === '晴')
        body.style.backgroundImage = 'url(../static/img/weather_background/night_sunny.jpg)';
    else if (time && weather === '多云')
        body.style.backgroundImage = 'url(../static/img/weather_background/day_cloudy.jpg)';
    else if (!time && weather === '多云')
        body.style.backgroundImage = 'url(../static/img/weather_background/night_cloudy.jpg)';
    else if (time && weather === '阴')
        body.style.backgroundImage = 'url(../static/img/weather_background/day_overcast.jpg)';
    else if (!time && weather === '阴')
        body.style.backgroundImage = 'url(../static/img/weather_background/night_overcast.jpg)';
    else if (time && weather.includes('雨'))
        body.style.backgroundImage = 'url(../static/img/weather_background/day_rain.jpg)';
    else if (!time && weather.includes('雨'))
        body.style.backgroundImage = 'url(../static/img/weather_background/night_rain.jpg)';
    else if (time && weather.includes('雪'))
        body.style.backgroundImage = 'url(../static/img/weather_background/day_snow.jpg)';
    else if (!time && weather.includes('雪'))
        body.style.backgroundImage = 'url(../static/img/weather_background/night_snow.jpeg)';
    else if (weather === '雾' || weather === '沙尘暴')
        body.style.backgroundImage = 'url(../static/img/weather_background/fog.jpeg)';
    else body.style.backgroundImage = 'url(../static/img/weather_background/default.jpg)';
}