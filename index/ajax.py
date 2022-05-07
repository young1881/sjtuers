from django.http import JsonResponse,HttpResponse

from .models import Site, SimpleMode, Wallpaper, User, Countdown


def img_upload(request):
    jaccount=request.session['jaccount']
    file_img = request.FILES['upload_file']  # 获取文件对象
    file_name = request.FILES['upload_file'].name
    print(file_name)
    username = request.POST.get('img_upload_username')
    # if not Wallpaper.objects.filter(user=jaccount):
    #     Wallpaper.objects.create(username=username, photo=file_img, photo_name=file_name)
    # else:
    wallpaper = Wallpaper.objects.filter(user=jaccount)[0]
    wallpaper.photo = file_img
    wallpaper.photo_name = file_name
    wallpaper.css = ""
    wallpaper.save()
    try:
        return JsonResponse(1, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse(0, safe=False)


def add_site(request):
    jaccount = request.session['jaccount']
    user = User.objects.filter(jaccount=jaccount)[0]
    site_name = request.POST.get('site_name')
    site_url = request.POST.get('site_url')
    site = Site.objects.filter(site_url=site_url, user=jaccount)
    if not site_url.startswith("http"):
        site_url = "https://" + site_url
    if site_url[-1] == "/":
        pass
    else:
        site_url = site_url + '/'

    if site:
        site[0].is_active = True
        site[0].save()
    elif ('sjtu' in site_url):
        site_src = '../static/img/school.png'
        Site.objects.create(user=user, site_name=site_name, site_url=site_url, site_src=site_src)
    else:
        site_src = site_url + 'favicon.ico'
        Site.objects.create(user=user, site_name=site_name, site_url=site_url, site_src=site_src)
    return HttpResponse("已保存")


def refactor_site(request):
    jaccount=request.session['jaccount']
    site_name = request.POST.get('refactor_site_name')
    site_url = request.POST.get('refactor_site_url')
    site = Site.objects.filter(user=jaccount, site_url=site_url)[0]
    site.site_name = site_name
    site.save()
    return HttpResponse("已保存")


def delete_site(request):
    jaccount=request.session['jaccount']
    # print(f"jaccount:{jaccount}")
    delete_site_name = request.POST.get('delete_site_name')
    site = Site.objects.filter(user=jaccount,site_name=delete_site_name)[0]
    site.is_active = False
    site.save()
    return HttpResponse("删除成功")


def simple_mode(request):
    jaccount=request.session['jaccount']
    # username = request.POST.get('simple_mode_username')
    this_simple_mode = SimpleMode.objects.get(user=jaccount)
    is_active = request.POST.get('simple_mode_is_active')
    is_active = (is_active == "true")
    this_simple_mode.is_active = is_active
    this_simple_mode.save()
    return HttpResponse("已保存")


def color_wallpaper(request):
    jaccount=request.session['jaccount']
    # username = request.POST.get('color_wallpaper_username')
    wallpaper = Wallpaper.objects.filter(user=jaccount)[0]
    css = request.POST.get('css')
    wallpaper.css = css
    wallpaper.save()
    return HttpResponse("已保存")


def refactor_countdown(request):
    jaccount = request.session['jaccount']
    date_name = request.POST.get('refactor_date_name')
    year = request.POST.get('year')
    month = request.POST.get('month')
    day = request.POST.get('day')
    countdown = Countdown.objects.filter(user=jaccount)[0]
    countdown.date_name = date_name
    countdown.year = int(year)
    countdown.month = int(month)
    countdown.day = int(day)
    countdown.save()

    this_simple_mode = SimpleMode.objects.get(user=jaccount)
    this_simple_mode.is_active = True
    this_simple_mode.save()
    return HttpResponse("已保存")