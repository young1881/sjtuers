from django.contrib import admin
from django.urls import path
from . import views, ajax

urlpatterns = [
    path('', views.index_view, name='index'),
    path('upload_img/', ajax.img_upload),
    path('add_site/', ajax.add_site),
    path('refactor_site/', ajax.refactor_site),
    path('delete_site/', ajax.delete_site),
    path('color_wallpaper/', ajax.color_wallpaper),
    path('simple_mode/', ajax.simple_mode),
]
