from .models import Site


def initialize_site(user):
    Site.objects.create(site_name='Canvas', site_url='https://oc.sjtu.edu.cn/', site_src='../static/img/在线课程.png', user=user)
    Site.objects.create(site_name='教学信息', site_url='https://i.sjtu.edu.cn/', site_src='../static/img/教学信息.png', user=user)
    Site.objects.create(site_name='学生事务', site_url='https://affairs.sjtu.edu.cn/', site_src='../static/img/学生事务.png', user=user)
    Site.objects.create(site_name='交我办', site_url='https://my.sjtu.edu.cn/', site_src='../static/img/交我办.png', user=user)

    Site.objects.create(site_name='交大官网', site_url='https://www.sjtu.edu.cn/', site_src='../static/img/官网.png', user=user)
    Site.objects.create(site_name='研究生院', site_url='https://www.gs.sjtu.edu.cn/', site_src='../static/img/研究生网.png', user=user)
    Site.objects.create(site_name='交大邮箱', site_url='https://mail.sjtu.edu.cn/', site_src='../static/img/邮箱.png', user=user)
    Site.objects.create(site_name='交大云盘', site_url='https://jbox.sjtu.edu.cn/', site_src='../static/img/交大云盘.png', user=user)
    Site.objects.create(site_name='水源社区', site_url='https://shuiyuan.sjtu.edu.cn/', site_src='../static/img/水源.png', user=user)
    # Site.objects.create(site_name='正版软件', site_url='http://lic.si.sjtu.edu.cn/Default/index/', site_src='../static/img/正版软件.png', user=user)
    Site.objects.create(site_name='䇹政项目', site_url='https://chuntsung.sjtu.edu.cn/', site_src='../static/img/䇹政.png', user=user)
    Site.objects.create(site_name='创新实践', site_url='https://uitp.sjtu.edu.cn/', site_src='../static/img/大创.png', user=user)
    Site.objects.create(site_name='教学楼', site_url='https://ids.sjtu.edu.cn/', site_src='../static/img/教学楼.png', user=user)
    Site.objects.create(site_name='图书馆', site_url='https://www.lib.sjtu.edu.cn/', site_src='../static/img/图书馆.png', user=user)
    Site.objects.create(site_name='选课社区', site_url='https://course.sjtu.plus/', site_src='../static/img/选课社区.png', user=user)
    Site.objects.create(site_name='github', site_url='https://github.com/', site_src='https://files.codelife.cc/itab/search/github.svg', user=user)
    Site.objects.create(site_name='bilibili', site_url='https://bilibili.com/', site_src='https://files.codelife.cc/itab/search/bilibili.svg', user=user)
    Site.objects.create(site_name='知乎', site_url='https://www.zhihu.com/', site_src='https://files.codelife.cc/itab/search/zhihu.svg', user=user)
    Site.objects.create(site_name='豆瓣', site_url='https://www.douban.com/', site_src='https://files.codelife.cc/itab/search/douban.svg', user=user)
    Site.objects.create(site_name='淘宝', site_url='https://www.taobao.com/', site_src='https://www.taobao.com/favicon.ico', user=user)
    Site.objects.create(site_name='爱奇艺', site_url='https://www.iqiyi.com/', site_src='https://www.iqiyi.com/favicon.ico', user=user)
    Site.objects.create(site_name='一个木函', site_url='https://web.woobx.cn/', site_src='https://web.woobx.cn/favicon.ico', user=user)
    Site.objects.create(site_name='百度', site_url='https://www.baidu.com/', site_src='https://www.baidu.com/favicon.ico', user=user, is_active=False)
    Site.objects.create(site_name='搜狗', site_url='https://www.sogou.com/', site_src='https://www.sogou.com/favicon.ico', user=user, is_active=False)