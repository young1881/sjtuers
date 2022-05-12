from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from . import views, ajax

urlpatterns = [
    path('', views.index_view, name='index'),
    path('upload_img/', csrf_exempt(ajax.img_upload), name="uploda_img"),
    path('add_site/', ajax.add_site, name="add_site"),
    path('refactor_site/', ajax.refactor_site, name="refactor_site"),
    path('delete_site/', ajax.delete_site, name="delete_site"),
    path('color_wallpaper/', ajax.color_wallpaper, name="color_wallpaper"),
    path('simple_mode/', ajax.simple_mode, name="simple_mode"),
    path('refactor_countdown/', ajax.refactor_countdown, name="refactor_countdown"),
]
