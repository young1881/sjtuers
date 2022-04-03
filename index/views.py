from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
import json
from time import time
from lxml import etree


def get_json(url):
    session = requests.Session()
    session.trust_env = False
    request = session.get(url)
    data = json.loads(request.content, strict=False)

    return data


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62',
    }

    session = requests.Session()
    session.trust_env = False
    response = session.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    return html


def lib():
    session = requests.Session()
    session.trust_env = False
    request = session.get(url)
    data = json.loads(request.content[12:-2], strict=False)['numbers']

    return data


def jwc():
    html = get_html('https://jwc.sjtu.edu.cn/xwtg/tztg.htm')
    tree = etree.HTML(html)
    a_list = tree.xpath('//div[@class="wz"]/a')
    jwc = []
    for i in range(5):
        title = str(i + 1) + ' ' + a_list[i].xpath('./h2/text()')[0]
        if len(title) > 25:
            title = title[:23] + '...'
        url = 'http://jwc.sjtu.edu.cn' + a_list[i].xpath('./@href')[0][2:]
        dic = {}
        dic['title'] = title
        dic['url'] = url
        jwc.append(dic)
    return jwc


def bilibli():
    json = get_json('https://api.bilibili.com/x/web-interface/popular?ps=5&pn=1')['data']['list']
    bilibili = []
    for i in range(5):
        dic = {}
        dic['title'] = str(i + 1) + ' ' + json[i]['title']
        if len(dic['title']) > 18:
            dic['title'] = dic['title'][:16] + '...'
        dic['url'] = json[i]['short_link']
        dic['view'] = json[i]['stat']['view']
        bilibili.append(dic)
    return bilibili


def index_view(request):
    if request.method == 'GET':

        weibo = get_json('https://tenapi.cn/resou/')['list']
        for i in range(len(weibo)):
            weibo[i]['name'] = str(i+1) + ' '+ weibo[i]['name']
            if len(weibo[i]['name']) > 18:
                weibo[i]['name'] = weibo[i]['name'][:16] + '...'

        zhihu = get_json('https://tenapi.cn/zhihuresou/')['list']
        for i in range(len(zhihu)):
            zhihu[i]['query'] = str(i + 1) + ' ' + zhihu[i]['query']
            if len(zhihu[i]['query']) > 22:
                zhihu[i]['query'] = zhihu[i]['query'][:20] + '...'

        corona = get_json('https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf')['data']["diseaseh5Shelf"]
        poem = get_json('https://v1.jinrishici.com/all.json')
        canteen = get_json('https://canteen.sjtu.edu.cn/CARD/Ajax/Place')
        library = get_json('http://zgrstj.lib.sjtu.edu.cn/cp?callback=CountPerson')[12:-2]

        locals = {
            'weibo' : weibo[:5],
            'zhihu' : zhihu[:5],
            'corona' : corona,
            'poem' : poem,
            'canteen' : canteen,
            'lib' : lib(),
            'jwc' : jwc(),
            'bilibili' : bilibli(),
        }

        return render(request, 'websites.html', locals)
