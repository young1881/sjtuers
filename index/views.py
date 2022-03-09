from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def index_view(request):
    if request.method == 'GET':
        import requests
        import json

        # 微博热搜数据
        weibo_request = requests.get('https://tenapi.cn/resou/')
        weibo = json.loads(weibo_request.content)['list']
        for i in range(len(weibo)):
            weibo[i]['name'] = str(i+1) + '  '+ weibo[i]['name']
            if len(weibo[i]['name']) > 18:
                weibo[i]['name'] = weibo[i]['name'][:16] + '...'

        # 知乎热搜数据
        zhihu_request = requests.get('https://tenapi.cn/zhihuresou/')
        zhihu = json.loads(zhihu_request.content)['list']
        for i in range(len(zhihu)):
            zhihu[i]['query'] = str(i + 1) + '  ' + zhihu[i]['query']
            if len(zhihu[i]['query']) > 22:
                zhihu[i]['query'] = zhihu[i]['query'][:20] + '...'

        local = {
            'weibo' : weibo[:5],
            'zhihu' : zhihu[:5],
        }

        return render(request, 'websites.html', local)

    elif request.method == 'POST':
        search_msg = request.POST['search_msg']
        if search_msg == '':
            baidu = "http://www.baidu.com/"
        else:
            baidu = "http://www.baidu.com/s?word=" + search_msg
        return HttpResponseRedirect(baidu)