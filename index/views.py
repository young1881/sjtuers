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
    request = session.get('https://zgrstj.lib.sjtu.edu.cn/cp?callback=CountPerson')
    data = json.loads(request.content[12:-2], strict=False)['numbers']

    return data


def jwc():
    html = get_html('https://jwc.sjtu.edu.cn/xwtg/tztg.htm')
    tree = etree.HTML(html)
    a_list = tree.xpath('//div[@class="wz"]/a')
    jwc = []
    for i in range(5):
        title = str(i + 1) + ' ' + a_list[i].xpath('./h2/text()')[0]
        if len(title) > 23:
            title = title[:21] + '...'
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


def weibo():
    weibo = get_json('https://tenapi.cn/resou/')['list']
    for i in range(len(weibo)):
        weibo[i]['name'] = str(i + 1) + ' ' + weibo[i]['name']
        if len(weibo[i]['name']) > 18:
            weibo[i]['name'] = weibo[i]['name'][:16] + '...'
    return weibo[:5]


def zhihu():
    zhihu = get_json('https://tenapi.cn/zhihuresou/')['list']
    for i in range(len(zhihu)):
        zhihu[i]['query'] = str(i + 1) + ' ' + zhihu[i]['query']
        if len(zhihu[i]['query']) > 22:
            zhihu[i]['query'] = zhihu[i]['query'][:20] + '...'
    return zhihu[:5]


def weather(city):
    url = "http://wthrcdn.etouch.cn/WeatherApi?city=" + city
    data = get_html(url)
    parser = etree.XMLParser(resolve_entities=False, strip_cdata=False, recover=True, ns_clean=True)
    XML_tree = etree.fromstring(data.encode(), parser=parser)

    forecast_list = XML_tree.xpath('//forecast/weather')
    forecast_dic = {}
    for i in range(len(forecast_list)):
        day_name = 'day' + str(i)
        forecast_dic[day_name] = {}
        forecast_dic[day_name]['date'] = '周' + forecast_list[i].xpath('./date/text()')[0][-1]
        forecast_dic[day_name]['high'] = forecast_list[i].xpath('./high/text()')[0][-3:-1]
        forecast_dic[day_name]['low'] = forecast_list[i].xpath('./low/text()')[0][-3:-1]
        forecast_dic[day_name]['type'] = forecast_list[i].xpath('.//type/text()')[0]
    forecast_dic['day0']['date'] = '今天'

    index_list = XML_tree.xpath('//zhishus/zhishu')
    index_dic = {}
    for i in range(len(index_list)):
        index_name = 'index' + str(i + 1)
        index_dic[index_name] = {}
        index_dic[index_name]['name'] = index_list[i].xpath('./name/text()')[0]
        index_dic[index_name]['value'] = index_list[i].xpath('./value/text()')[0]
        index_dic[index_name]['detail'] = index_list[i].xpath('./detail/text()')[0]

    weather = {
        'city': XML_tree.xpath('//city/text()')[0],
        'updatetime': XML_tree.xpath('//updatetime/text()')[0],
        'fengli': XML_tree.xpath('//fengli/text()')[0],
        'wendu': XML_tree.xpath('//wendu/text()')[0],
        'shidu': XML_tree.xpath('//shidu/text()')[0],
        'fengxiang': XML_tree.xpath('//fengxiang/text()')[0],
        'sunrise': XML_tree.xpath('//sunrise_1/text()')[0],
        'sunset': XML_tree.xpath('//sunset_1/text()')[0],
        'yesterday': {
            'date': '昨天',
            'high': XML_tree.xpath('//high_1/text()')[0][-3:-1],
            'low': XML_tree.xpath('//low/text()')[0][-3:-1],
            'type': XML_tree.xpath('//type_1/text()')[0]
        },
        'forecast': forecast_dic,
        'index': index_dic,
    }
    return weather


def index_view(request):
    if request.method == 'GET':
        corona = get_json('https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf')['data']["diseaseh5Shelf"]
        poem = get_json('https://v1.jinrishici.com/all.json')
        canteen = get_json('https://canteen.sjtu.edu.cn/CARD/Ajax/Place')

        locals = {
            'weibo' : weibo(),
            'zhihu' : zhihu(),
            'corona' : corona,
            'poem' : poem,
            'canteen' : canteen,
            'lib' : lib(),
            'jwc' : jwc(),
            'bilibili' : bilibli(),
            'weather' : weather('上海'),
        }

        return render(request, 'websites.html', locals)
