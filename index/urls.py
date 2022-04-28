from django.contrib import admin
from django.urls import path
from . import views, views_ajax

urlpatterns = [
    path('', views.index_view, name='index'),
    path('upload_img/', views_ajax.img_upload),
    path('add_website/', views_ajax.img_upload),
]
