from django.shortcuts import render
import asyncio
import json
from lxml import etree
from urllib.parse import quote
import aiohttp

def index_view(request):
    if request.method == 'GET':
        city = '闵行'
        names = [
            'jwc',
            'weather',
            'weibo',
            'zhihu',
            'bilibili',
            'corona',
            'poem',
            'canteen',
            'lib',
        ]
        urls = [
            'https://jwc.sjtu.edu.cn/xwtg/tztg.htm',
            'http://wthrcdn.etouch.cn/WeatherApi?city=' + quote(city),
            'https://tenapi.cn/resou/',
            'https://tenapi.cn/zhihuresou/',
            'https://api.bilibili.com/x/web-interface/popular?ps=5&pn=1',
            'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf',
            'https://v1.jinrishici.com/all.json',
            'https://canteen.sjtu.edu.cn/CARD/Ajax/Place',
            'https://zgrstj.lib.sjtu.edu.cn/cp?callback=CountPerson',
        ]
        urls_names = {}
        for i in range(len(urls)):
            urls_names[urls[i]] = names[i]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62',
        }
        responses = {}

        # 异步编程
        async def fetch(session, url):
            print("发送请求：", url)
            async with session.get(url, headers=headers) as response:
                assert response.status == 200
                page_text = await response.text()
                url = str(response.url)
                name = urls_names[url]
                responses[name] = page_text

        async def main():
            async with aiohttp.ClientSession() as session:
                tasks = [asyncio.create_task(fetch(session, url)) for url in urls]
                await asyncio.wait(tasks)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())

        print('数据获取结束，接下来处理数据')
        locals = {
            'jwc': jwc(responses['jwc']),
            'weather': weather(responses['weather']),
            'weibo': weibo(responses['weibo']),
            'zhihu': zhihu(responses['zhihu']),
            'bilibili': bilibli(responses['bilibili']),
            'corona': corona(responses['corona']),
            'poem': poem(responses['poem']),
            'canteen': canteen(responses['canteen']),
            'lib': lib(responses['lib']),
        }
        return render(request, 'websites.j2', locals)


def get_json(response):
    data = json.loads(response, strict=False)
    return data


def get_html(response):
    return response


def lib(response):
    data = json.loads(response[12:-2], strict=False)['numbers']
    return data


def jwc(response):
    html = get_html(response)
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


def bilibli(response):
    json = get_json(response)['data']['list']
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


def weibo(response):
    weibo = get_json(response)['list']
    for i in range(len(weibo)):
        weibo[i]['name'] = str(i + 1) + ' ' + weibo[i]['name']
        if len(weibo[i]['name']) > 18:
            weibo[i]['name'] = weibo[i]['name'][:16] + '...'
    return weibo[:5]


def zhihu(response):
    zhihu = get_json(response)['list']
    for i in range(len(zhihu)):
        zhihu[i]['query'] = str(i + 1) + ' ' + zhihu[i]['query']
        if len(zhihu[i]['query']) > 22:
            zhihu[i]['query'] = zhihu[i]['query'][:20] + '...'
    return zhihu[:5]


def weather(response):
    data = get_html(response)
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


def corona(response):
    return get_json(response)['data']["diseaseh5Shelf"]


def poem(response):
    return get_json(response)


def canteen(response):
    return get_json(response)
