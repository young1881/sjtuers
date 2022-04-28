from django.contrib import admin

# Register your models here.
from .models import Site, SimpleMode, User, Wallpaper


class UserManager(admin.ModelAdmin):
    list_display = ['user_name','jaccount']
    list_display_links = ['user_name']
    search_fields = ['user_name']


admin.site.register(User, UserManager)

class SiteManager(admin.ModelAdmin):
    list_display = ['user','site_name','site_url','site_src','is_active']
    list_display_links = ['site_name']
    search_fields = ['site_name']


admin.site.register(Site, SiteManager)


class SimpleModeManager(admin.ModelAdmin):
    list_display = ['username','is_active']
    list_display_links = ['username']
    search_fields = ['username']

admin.site.register(SimpleMode, SimpleModeManager)


class WallpaperManager(admin.ModelAdmin):
    list_display = ['username','photo','photo_name']
    list_display_links = ['photo_name']
    search_fields = ['photo_name']

admin.site.register(Wallpaper, WallpaperManager)