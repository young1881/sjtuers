var info_btns = document.getElementsByClassName("info_btn")
var infos = document.getElementsByClassName("info")

for (var i = 0; i < info_btns.length; i++) {
    info_btns[i].index = i;
    info_btns[i].onclick = function () {
        for (var j = 0; j < info_btns.length; j++) {
            info_btns[j].className = info_btns[j].className.replace(' active', '').trim();
            infos[j].className = infos[j].className.replace(' show', '').trim();
        }
        this.className = this.className + ' active';
        infos[this.index].className = infos[this.index].className + ' show';
    };
}

var tool_btns = document.getElementsByClassName("tool_btn")
var tools = document.getElementsByClassName("tool")

for (var i = 0; i < tool_btns.length; i++) {
    tool_btns[i].index = i;
    tool_btns[i].onclick = function () {
        for (var j = 0; j < tool_btns.length; j++) {
            tool_btns[j].className = tool_btns[j].className.replace(' active', '').trim();
            tools[j].className = tools[j].className.replace(' show', '').trim();
        }
        this.className = this.className + ' active';
        tools[this.index].className = tools[this.index].className + ' show';
    };
}