from django.http import JsonResponse,HttpResponse

from .models import Site, SimpleMode, Wallpaper


def img_upload(request):
    file_img = request.FILES['img']  # 获取文件对象
    image = Wallpaper()
    image.photo = file_img
    try:
        image.save()  # 保存数据
        return JsonResponse(1, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse(0, safe=False)


def add_site(request):
    site_name = request.POST.get('site_name')
    site_url = request.POST.get('site_url')
    if not site_url.startswith("http"):
        site_url = "https://" + site_url
    if site_url[-1] == "/":
        site_src = site_url + 'favicon.ico'
    else:
        site_src = site_url + '/favicon.ico'
    Site.objects.create(site_name=site_name, site_url=site_url, site_src=site_src)
    return HttpResponse("已保存")


def refactor_site(request):
    site_name = request.POST.get('refactor_site_name')
    site_url = request.POST.get('refactor_site_url')
    site = Site.objects.filter(site_url=site_url)[0]
    site.site_name = site_name
    site.save()
    return HttpResponse("已保存")


def delete_site(request):
    delete_site_name = request.POST.get('delete_site_name')
    site = Site.objects.filter(site_name=delete_site_name)[0]
    site.is_active = False
    site.save()
    return HttpResponse("删除成功")


def simple_mode(request):
    username = request.POST.get('simple_mode_username')
    this_simple_mode = SimpleMode.objects.get(username=username)
    is_active = request.POST.get('simple_mode_is_active')
    is_active = (is_active == "true")
    this_simple_mode.is_active = is_active
    this_simple_mode.save()
    return HttpResponse("已保存")


def color_wallpaper(request):
    username = request.POST.get('color_wallpaper_username')
    wallpaper = Wallpaper.objects.filter(username=username)[0]
    css = request.POST.get('css')
    wallpaper.css = css
    wallpaper.save()
    return HttpResponse("已保存")