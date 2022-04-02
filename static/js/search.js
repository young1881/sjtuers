$(function () {
    var search = {
        data: [
            { name: '百度', img: 'https://www.baidu.com/favicon.ico', url: 'https://www.baidu.com/s?wd=' },
            { name: '谷歌', img: 'https://www.google.com/favicon.ico', url: 'https://www.google.com/search?q=' },
            { name: '必应', img: 'https://cn.bing.com/favicon.ico', url: 'https://cn.bing.com/search?q=' },
            { name: '搜狗', img: 'https://www.sogou.com/favicon.ico', url: 'https://www.sogou.com/web?query=' },
            { name: '知乎', img: 'https://www.zhihu.com/favicon.ico', url: 'https://www.zhihu.com/search?q=' },
            { name: '有道', img: 'https://dict.youdao.com/favicon.ico', url: 'https://dict.youdao.com/w/eng/' },
            { name: 'B站', img: 'https://search.bilibili.com/favicon.ico', url: 'https://search.bilibili.com/all?keyword=' },
            { name: 'CSDN', img: 'https://so.csdn.net/favicon.ico', url: 'https://so.csdn.net/so/search/s.do?q=' },
            { name: 'Github', img: 'https://github.com/favicon.ico', url: 'https://github.com/search?q=' },
        ]
    };
    for (var i = 0; i < search.data.length; i++) {
        var addList = '<li><img src="' + search.data[i].img + '"/>' + search.data[i].name + '</li>';
        $('.search-engine-list').append(addList)
    }
    $('.engine, .search-engine').hover(
        function () {
            $('.search-engine').css('display', 'block')
        },
        function () {
            $('.search-engine').css('display', 'none')
        }
    );
    var thisSearch = 'https://www.baidu.com/s?wd=';
    var thisImg = 'https://www.baidu.com/favicon.ico';
    $('.search-engine-list li').click(
        function () {
            var _index = $(this).index();
            thisImg = $(this).children().attr('src');
            $('.engine').attr('src', thisImg);
            thisSearch = search.data[_index].url;
            $('.search-engine').css('display', 'none');
        }
    )
    $('#search-button').click(
        function () {
            var textValue = $('#text').val();
            var textValue = textValue.replace(/\%/g, "%25");
            var textValue = textValue.replace(/\+/g, "%2B");
            var textValue = textValue.replace(/\//g, "%2F");
            var textValue = textValue.replace(/\?/g, "%3F");
            var textValue = textValue.replace(/\&/g, "%26");
            var textValue = textValue.replace(/\=/g, "%3D");
            var textValue = textValue.replace(/\#/g, "%23");
            window.open(thisSearch + textValue, thisSearch + textValue);
        }
    );
});