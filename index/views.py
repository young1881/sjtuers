from os import access
from django.shortcuts import render
from django.http import HttpResponse
import asyncio
import json
from lxml import etree
from urllib.parse import quote
import aiohttp
import time
import requests
from .models import Site, SimpleMode

def index_view(request):
    request_time = time.time()
    city = '闵行'
    names = [
        'jwc',
        'jnews',
        'weather',
        'weibo',
        'zhihu',
        'bilibili',
        'corona',
        'poem',
        'canteen',
        'lib',
        # 'jac'
    ]
    urls = [
        'https://jwc.sjtu.edu.cn/xwtg/tztg.htm',
        'https://www.sjtu.edu.cn/',
        'http://wthrcdn.etouch.cn/WeatherApi?city=' + quote(city),
        'https://tophub.today/n/KqndgxeLl9',
        'https://tophub.today/n/mproPpoq6O',
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
        async with session.get(url=url, headers=headers) as response:
            assert response.status == 200
            page_text = await response.text()
            url = str(response.url)
            name = urls_names[url]
            responses[name] = page_text

    async def main():
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, verify_ssl=False)) as session:
            tasks = [asyncio.create_task(fetch(session, url)) for url in urls]
            await asyncio.wait(tasks)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

    try:
        result = jac(request)
        result = result['entities'][0]['name']
        simple_mode_flag = SimpleMode.objects.filter(username=result)
        if not simple_mode_flag:
            SimpleMode.objects.create(username=result)
        simple_mode = {'username': result, 'is_active': simple_mode_flag[0].is_active}
    except:
        result = ''
        SimpleMode.objects.create()
        simple_mode = {'username': 'visitor', 'is_active': False}
        print(f"Please login!")


    response_time = time.time()
    print('数据获取结束，共用时', response_time-request_time, 's')

    sites = Site.objects.filter(is_active=True)

    locals = {
        'jwc': jwc(responses['jwc']),
        'jnews': jnews(responses['jnews']),
        'weather': weather(responses['weather']),
        'weibo': weibo(responses['weibo']),
        'zhihu': zhihu(responses['zhihu']),
        'bilibili': bilibli(responses['bilibili']),
        'corona': corona(responses['corona']),
        'poem': poem(responses['poem']),
        'canteen': canteen(responses['canteen']),
        'lib': lib(responses['lib']),
        'sites': sites,
        'jac': result,
        'simple_mode' : simple_mode,
    }

    process_time = time.time()
    print('数据处理结束，共用时', process_time - response_time, 's')

    if request.method == 'GET':
        return render(request, 'websites.j2', locals)
    elif request.method == 'POST':
        if request.POST.get('site_name') != None:
            site_name = request.POST.get('site_name')
            site_url = request.POST.get('site_url')
            if site_url.startswith("http") != True:
                site_url = "https://" + site_url
            if site_url[-1] == "/":
                site_src = site_url + 'favicon.ico'
            else:
                site_src = site_url + '/favicon.ico'
            Site.objects.create(site_name=site_name, site_url=site_url, site_src=site_src)

        if request.POST.get('refactor_site_name') != None:
            site_name = request.POST.get('refactor_site_name')
            site_url = request.POST.get('refactor_site_url')
            if Site.objects.filter(site_name=site_name):
                site = Site.objects.filter(site_name=site_name)[0]
                site.site_url = site_url
                site.save()
            if Site.objects.filter(site_url=site_url):
                site = Site.objects.filter(site_url=site_url)[0]
                site.site_name = site_name
                site.save()

        if request.POST.get('delete_site_name') != None:
            print("收到")
            delete_site = request.POST.get('delete_site_name')
            site = Site.objects.get(site_name=delete_site)
            site.is_active = False
            site.save()
            return HttpResponse("删除成功")

        if request.POST.get('simple_mode_username') != None:
            username = request.POST.get('simple_mode_username')
            print(username)
            simple_mode = SimpleMode.objects.get(username=username)
            is_active = request.POST.get('simple_mode_is_active')
            is_active = (is_active == "true")
            simple_mode.is_active = is_active
            print(simple_mode.is_active)
            simple_mode.save()
            return HttpResponse("已保存")

        sites = Site.objects.filter(is_active=True)
        locals['sites'] = sites
        return render(request, 'websites.j2', locals)

# 按字符实际长度截取，一个汉字长度为2，一个字母/数字长度为1
def cut_str(str, len):
    bytes = str.encode('utf-8')
    cut_tmp = bytes[:len]
    cut_res = cut_tmp.decode('utf-8', errors='ignore')  # 按bytes截取时有小部分无效的字节，传入errors='ignore'忽略错误
    return cut_res


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
        if len(title.encode('utf-8')) > 55:
            title = cut_str(title, 53) + '...'
        url = 'http://jwc.sjtu.edu.cn' + a_list[i].xpath('./@href')[0][2:]
        dic = {}
        dic['title'] = title
        dic['url'] = url
        jwc.append(dic)
    return jwc


def jnews(response):
    html = get_html(response)
    tree = etree.HTML(html)
    a_list = tree.xpath('//div[@class="new-add-list  clearfix"]//ul[1]//a')
    jnews = []
    for i in range(5):
        title = str(i + 1) + ' ' + a_list[i].xpath('./text()')[0]
        if len(title.encode('utf-8')) > 55:
            title = cut_str(title, 53) + '...'
        url = a_list[i].xpath('./@href')[0]
        dic = {}
        dic['title'] = title
        dic['url'] = url
        jnews.append(dic)
    return jnews


def bilibli(response):
    json = get_json(response)['data']['list']
    bilibili = []
    for i in range(5):
        dic = {}
        dic['title'] = str(i + 1) + ' ' + json[i]['title']
        if len(dic['title'].encode("utf-8")) > 50:
            dic['title'] = cut_str(dic['title'], 48) + '...'
        dic['url'] = json[i]['short_link']
        dic['view'] = json[i]['stat']['view']
        bilibili.append(dic)
    return bilibili


def weibo(response):
    html = get_html(response)
    tree = etree.HTML(html)
    tr_list = tree.xpath('//tbody/tr')[:5]
    weibo = []
    for i in range(len(tr_list)):
        weibo_item = {}
        name = tr_list[i].xpath('./td[@class="al"]/a/text()')[0]
        name = str(i + 1) + ' ' + name
        if len(name.encode('utf-8')) > 50:
            name = cut_str(name, 48) + '...'
        url = 'https://tophub.today' + tr_list[i].xpath('./td[@class="al"]/a/@href')[0]
        hot = tr_list[i].xpath('./td[3]/text()')[0]
        weibo_item['name'] = name
        weibo_item['url'] = url
        weibo_item['hot'] = hot
        weibo.append(weibo_item)
    return weibo


def zhihu(response):
    html = get_html(response)
    tree = etree.HTML(html)
    tr_list = tree.xpath('//tbody/tr')[:5]
    zhihu = []
    for i in range(len(tr_list)):
        zhihu_item = {}
        name = tr_list[i].xpath('./td[@class="al"]/a/text()')[0]
        name = str(i + 1) + ' ' + name
        if len(name.encode('utf-8')) > 55:
            name = cut_str(name, 53) + "..."
        url = 'https://tophub.today' + tr_list[i].xpath('./td[@class="al"]/a/@href')[0]
        zhihu_item['name'] = name
        zhihu_item['url'] = url
        zhihu.append(zhihu_item)
    return zhihu


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


def jac(request):
    token = request.session['token']
    access_token = token['access_token']
    # print(f"token:{token['access_token']}")
    result = requests.get(f'https://api.sjtu.edu.cn/v1/me/profile?access_token={access_token}')
    print(f"result:{result.json()}")
    return result.json()