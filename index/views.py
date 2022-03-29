from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def index_view(request):
    if request.method == 'GET':

        # 微博热搜数据
        weibo = get_data('https://tenapi.cn/resou/')['list']
        for i in range(len(weibo)):
            weibo[i]['name'] = str(i+1) + '  '+ weibo[i]['name']
            if len(weibo[i]['name']) > 18:
                weibo[i]['name'] = weibo[i]['name'][:16] + '...'

        # 知乎热搜数据
        zhihu = get_data('https://tenapi.cn/zhihuresou/')['list']
        for i in range(len(zhihu)):
            zhihu[i]['query'] = str(i + 1) + '  ' + zhihu[i]['query']
            if len(zhihu[i]['query']) > 22:
                zhihu[i]['query'] = zhihu[i]['query'][:20] + '...'

        #疫情数据
        corona = get_data('https://lab.isaaclin.cn//nCoV/api/overall')['results'][0]

        #诗句
        poem = get_data('https://v1.jinrishici.com/all.json')

        local = {
            'weibo' : weibo[:5],
            'zhihu' : zhihu[:5],
            'corona': corona,
            'poem': poem,
        }

        return render(request, 'websites.html', local)

def get_data(url):
    import requests
    import json

    session = requests.Session()
    session.trust_env = False
    request = session.get(url)
    data = json.loads(request.content)

    return data