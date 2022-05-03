from django.contrib import admin
from django.urls import path
from . import views, views_ajax

urlpatterns = [
    path('', views.index_view, name='index'),
    path('upload_img/', views_ajax.img_upload),
    path('add_site/', views_ajax.add_site),
    path('refactor_site/', views_ajax.refactor_site),
    path('delete_site/', views_ajax.delete_site),
    path('color_wallpaper/', views_ajax.color_wallpaper),
    path('simple_mode/', views_ajax.simple_mode),
]
