from django.http import JsonResponse

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