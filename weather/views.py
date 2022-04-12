from django.shortcuts import render
import requests
from lxml import etree

# Create your views here.
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

def weather_view(request):
    data = get_html("http://wthrcdn.etouch.cn/WeatherApi?city=%E4%B8%8A%E6%B5%B7")
    parser = etree.XMLParser(resolve_entities=False, strip_cdata=False, recover=True, ns_clean=True)
    XML_tree = etree.fromstring(data.encode(), parser=parser)

    forecast_list = XML_tree.xpath('//forecast/weather')
    forecast_dic = {}
    for i in range(len(forecast_list)):
        day_name = 'day+' + str(i)
        forecast_dic[day_name] = {}
        forecast_dic[day_name]['date'] = forecast_list[i].xpath('./date/text()')[0]
        forecast_dic[day_name]['high'] = forecast_list[i].xpath('./high/text()')[0]
        forecast_dic[day_name]['low'] = forecast_list[i].xpath('./low/text()')[0]
        forecast_dic[day_name]['type'] = forecast_list[i].xpath('.//type/text()')[0]

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
        'yesterday':{
            'date': XML_tree.xpath('//date_1/text()')[0],
            'high': XML_tree.xpath('//high_1/text()')[0],
            'low': XML_tree.xpath('//low/text()')[0],
        },
        'forecast': forecast_dic,
        'index' : index_dic,
    }

    return render(request, 'weather.html', weather)