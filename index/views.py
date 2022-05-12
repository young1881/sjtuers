from django.shortcuts import render
import asyncio
import json
from lxml import etree
from urllib.parse import quote
import aiohttp
import time
import datetime
import requests
from .models import Site, SimpleMode, User, Wallpaper, Countdown
from .initialize_site import initialize_site
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport
from django.http import HttpResponse, HttpResponseRedirect
from .models import Site, SimpleMode
from random import randrange
from django.http import HttpResponse
from rest_framework.views import APIView
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.options.global_options import ThemeType

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
    ]
    urls = [
        'https://jwc.sjtu.edu.cn/xwtg/tztg.htm',
        'https://www.sjtu.edu.cn/',
        'http://wthrcdn.etouch.cn/WeatherApi?city=' + quote(city),
        # 'https://tenapi.cn/resou/',
        # 'https://tenapi.cn/zhihuresou/',
        'https://tophub.today/n/KqndgxeLl9',
        'https://tophub.today/n/mproPpoq6O',
        'https://api.bilibili.com/x/web-interface/popular?ps=5&pn=1',
        'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf',
        'https://v1.jinrishici.com/all.json',
        'https://canteen.sjtu.edu.cn/CARD/Ajax/Place',
        'https://zgrstj.lib.sjtu.edu.cn/cp?callback=CountPerson',
    ]
    urls_names = dict(zip(urls, names))
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

    # 初始化default用户
    jaccount_default_flag = User.objects.filter(jaccount='000')
    if not jaccount_default_flag:
        User.objects.create(jaccount='000')
        user = User.objects.filter(jaccount='000')[0]
        SimpleMode.objects.create(user=user)
        Wallpaper.objects.create(user=user)
        Countdown.objects.create(user=user)
        initialize_site(user)

    try:
        result_origin = jac(request)
        result = result_origin['entities'][0]['name']
        jaccount = result_origin['entities'][0]['account']
        jaccount_flag = User.objects.filter(jaccount=jaccount)

        # 如果这个Jac用户第一次登录，则在数据库的User表中新建一条记录
        # 并且复制default用户的所有网站，作为初始设置
        if not jaccount_flag:
            User.objects.create(user_name=result, jaccount=jaccount)
            user = User.objects.filter(jaccount=jaccount)[0]
            SimpleMode.objects.create(user=user, username=result, is_active=False)
            Wallpaper.objects.create(user=user, username=result)
            Countdown.objects.create(user=user, username=result)
            user_site_flag = Site.objects.filter(user='000')
            for site in user_site_flag:
                Site.objects.create(site_name=site.site_name, site_url=site.site_url, site_src=site.site_src, user=user,
                                    is_active=site.is_active)

        user = User.objects.filter(jaccount=jaccount)[0]
        simple_mode_flag = SimpleMode.objects.filter(user=jaccount)[0]
        simple_mode = {'user': user, 'username': result, 'is_active': simple_mode_flag.is_active}
        wallpaper_flag = Wallpaper.objects.filter(user=jaccount)[0]
        wallpaper = {'user': user,
                     'username': result,
                     'photo_url': '../media/wallpaper/' + wallpaper_flag.photo_name,
                     'photo_name': wallpaper_flag.photo_name,
                     'css': wallpaper_flag.css}

        countdown_flag = Countdown.objects.filter(user=jaccount)
        print(f"countdown_flag:{countdown_flag}")
        countdown_flag = Countdown.objects.filter(user=jaccount)[0]
        
        countdown = compute_countdown(countdown_flag.date_name, countdown_flag.year,
                                      countdown_flag.month, countdown_flag.day)
    except:
        result = ''
        jaccount = '000'
        user = User.objects.filter(jaccount='000')[0]
        simple_mode = {'user': user, 'username': 'visitor', 'is_active': False}
        wallpaper = {'user': user,
                     'username': "visitor",
                     'photo_url': '../media/wallpaper/visitor.jpg',
                     'photo_name': 'visitor.jpg',
                     "css": "linear-gradient(90deg, #70e1f5 0%, #ffd194 100%)"}
        countdown = compute_countdown("元旦", 2023, 1, 1)
        print(f"Please login!")
        print("except!")

    request.session['jaccount'] = jaccount

    response_time = time.time()
    print('数据获取结束，共用时', response_time - request_time, 's')

    sites = Site.objects.filter(user=jaccount, is_active=True)
    locals = {
        'jwc': jwc(responses['jwc']),
        'jnews': jnews(responses['jnews']),
        'weather': weather(responses['weather']),
        'weibo': weibo(responses['weibo']),
        'zhihu': zhihu(responses['zhihu']),
        'bilibili': bilibli(responses['bilibili']),
        'corona': corona(responses['corona']),
        'poem': poem(responses['poem']),
        'sites': sites,
        'jac': result,
        'simple_mode': simple_mode,
        "wallpaper": wallpaper,
        'countdown': countdown,
    }

    process_time = time.time()
    print('数据处理结束，共用时', process_time - response_time, 's')
    if request.method == 'GET':
        return render(request, 'websites.html', locals)


# 按字符实际长度截取，一个汉字长度为2，一个字母/数字长度为1
def cut_str(str_before, len_cut):
    to_bytes = str_before.encode('utf-8')
    cut_tmp = to_bytes[:len_cut]
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
    jwc_dic = []
    for i in range(5):
        title = str(i + 1) + ' ' + a_list[i].xpath('./h2/text()')[0]
        if len(title.encode('utf-8')) > 55:
            title = cut_str(title, 53) + '...'
        url = 'https://jwc.sjtu.edu.cn' + a_list[i].xpath('./@href')[0][2:]
        dic = {'title': title, 'url': url}
        jwc_dic.append(dic)
    return jwc_dic


def jnews(response):
    html = get_html(response)
    tree = etree.HTML(html)
    a_list = tree.xpath('//div[@class="new-add-list  clearfix"]//ul[1]//a')
    jnews_dic = []
    for i in range(5):
        title = str(i + 1) + ' ' + a_list[i].xpath('./text()')[0]
        if len(title.encode('utf-8')) > 55:
            title = cut_str(title, 53) + '...'
        url = a_list[i].xpath('./@href')[0]
        dic = {'title': title, 'url': url}
        jnews_dic.append(dic)
    return jnews_dic


def bilibli(response):
    bilibili_json = get_json(response)['data']['list']
    bilibili = []
    for i in range(5):
        dic = {'title': str(i + 1) + ' ' + bilibili_json[i]['title']}
        if len(dic['title'].encode("utf-8")) > 50:
            dic['title'] = cut_str(dic['title'], 48) + '...'
        dic['url'] = bilibili_json[i]['short_link']
        dic['view'] = bilibili_json[i]['stat']['view']
        bilibili.append(dic)
    return bilibili

# def weibo(response):
#     data = get_json(response)['list']
#     weibo_dict = []
#     for i in range(5):
#         name = data[i]['name']
#         name = str(i + 1) + ' ' + name
#         if len(name.encode('utf-8')) > 46:
#             name = cut_str(name, 44) + '...'
#         url = data[i]['url']
#         hot = data[i]['hot']
#         weibo_item = {'name': name, 'url': url, 'hot': hot}
#         weibo_dict.append(weibo_item)
#     return weibo_dict


# def zhihu(response):
#     data = get_json(response)['list']
#     zhihu_dict = []
#     for i in range(5):
#         name = data[i]['query']
#         name = str(i + 1) + ' ' + name
#         if len(name.encode('utf-8')) > 55:
#             name = cut_str(name, 53) + "..."
#         url = data[i]['url']
#         zhihu_item = {'name': name, 'url': url}
#         zhihu_dict.append(zhihu_item)
#     return zhihu_dict

# 代理网站爬取的函数
def weibo(response):
    html = get_html(response)
    tree = etree.HTML(html)
    tr_list = tree.xpath('//table/tbody/tr')[:5]
    weibo_dict = []
    for i in range(len(tr_list)):
        name = tr_list[i].xpath('./td[2]/a/text()')[0]
        name = str(i + 1) + ' ' + name
        if len(name.encode('utf-8')) > 46:
            name = cut_str(name, 44) + '...'
        url = 'https://tophub.today' + tr_list[i].xpath('./td[2]/a/@href')[0]
        hot = tr_list[i].xpath('./td[3]/text()')[0]
        weibo_item = {'name': name, 'url': url, 'hot': hot}
        weibo_dict.append(weibo_item)
    return weibo_dict


def zhihu(response):
    html = get_html(response)
    tree = etree.HTML(html)
    tr_list = tree.xpath('//tbody/tr')[:5]
    zhihu_dict = []
    for i in range(len(tr_list)):
        name = tr_list[i].xpath('./td[@class="al"]/a/text()')[0]
        name = str(i + 1) + ' ' + name
        if len(name.encode('utf-8')) > 55:
            name = cut_str(name, 53) + "..."
        url = 'https://tophub.today' + tr_list[i].xpath('./td[@class="al"]/a/@href')[0]
        zhihu_item = {'name': name, 'url': url}
        zhihu_dict.append(zhihu_item)
    return zhihu_dict

# def weibo(response):
#     data = get_json(response)['list']
#     weibo_dict = []
#     for i in range(5):
#         name = data[i]['name']
#         name = str(i + 1) + ' ' + name
#         if len(name.encode('utf-8')) > 46:
#             name = cut_str(name, 44) + '...'
#         url = data[i]['url']
#         hot = data[i]['hot']
#         weibo_item = {'name': name, 'url': url, 'hot': hot}
#         weibo_dict.append(weibo_item)
#     return weibo_dict
#
#
# def zhihu(response):
#     data = get_json(response)['list']
#     zhihu_dict = []
#     for i in range(5):
#         name = data[i]['query']
#         name = str(i + 1) + ' ' + name
#         if len(name.encode('utf-8')) > 55:
#             name = cut_str(name, 53) + "..."
#         url = data[i]['url']
#         zhihu_item = {'name': name, 'url': url}
#         zhihu_dict.append(zhihu_item)
#     return zhihu_dict


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

    weather_dict = {
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
    return weather_dict

def canteen():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62',
    }
    url = 'https://canteen.sjtu.edu.cn/CARD/Ajax/Place'
    session = requests.session()
    response = session.get(url=url, headers=headers).text
    return get_json(response)


def lib():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62',
    }
    url = 'https://zgrstj.lib.sjtu.edu.cn/cp?callback=CountPerson'
    session = requests.session()
    response = session.get(url=url, headers=headers).text
    data = json.loads(response[12:-2], strict=False)['numbers']
    return data

# 可视化
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error

# 餐厅
def can_bar() -> Bar:

    c = (
        Bar()
        .add_xaxis(["一餐", "一餐清真","二餐", "三餐", "三餐清真","四餐", "五餐", "哈乐","玉兰苑"])
        .add_yaxis("已取餐量", [canteen()[0]['Seat_u'],canteen()[1]['Seat_u'],canteen()[2]['Seat_u'],canteen()[3]['Seat_u'],canteen()[4]['Seat_u'],canteen()[5]['Seat_u'],canteen()[6]['Seat_u'],canteen()[7]['Seat_u'],canteen()[8]['Seat_u']],
                   category_gap="30%"
                   # stack='stack1'
                   )
        .add_yaxis("供应总量",[canteen()[0]['Seat_s'],canteen()[1]['Seat_s'],canteen()[2]['Seat_s'],canteen()[3]['Seat_s'],canteen()[4]['Seat_s'],canteen()[5]['Seat_s'],canteen()[6]['Seat_s'],canteen()[7]['Seat_s'],canteen()[8]['Seat_s']],
                   category_gap="30%"
                   # stack='stack1'
                   )
        # rotate 旋转角度
        .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30, interval=0,font_size=10)),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=7)))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))

        # .reversal_axis()
        .dump_options_with_quotes()
    )
    return c

def lib_bar() -> Bar:
    b = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(["图书馆主馆", "李政道图书馆","包玉刚图书馆", "徐汇社科馆"])
        .add_yaxis("在馆人数", [lib()[0]['inCounter'],lib()[1]['inCounter'],lib()[2]['inCounter'],lib()[3]['inCounter']],
                    category_gap="30%",
                    stack='stack1'
                   )
        .add_yaxis("可容纳人数", [lib()[0]['max'],lib()[1]['max'],lib()[2]['max'],lib()[3]['max']],
                   category_gap="30%",
                   stack='stack1'
                   )
        .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20, interval=0,font_size=11)))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        # .set_series_opts(label_opts=opts.LabelOpts(position='right', font_size = 16)
        .dump_options_with_quotes()
    )
    return b

class ChartView_can(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(can_bar()))

class IndexView_can(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/can_index.html").read())

class ChartView_lib(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(lib_bar()))
#
class IndexView_lib(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/lib_index.html").read())


def corona(response):
    return get_json(response)['data']["diseaseh5Shelf"]


def poem(response):
    return get_json(response)


def jac(request):
    token = request.session['token']
    access_token = token['access_token']

    result = requests.get(f'https://api.sjtu.edu.cn/v1/me/profile?access_token={access_token}', verify=False)
    return result.json()


def compute_countdown(date_name, year, month, day):
    d1 = datetime.date.today()
    d2 = datetime.date(year, month, day)
    interval = d2 - d1
    countdown = {'date_name': date_name, "interval": interval.days}
    return countdown


def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper


_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
