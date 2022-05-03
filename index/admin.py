from django.contrib import admin

# Register your models here.
from .models import Site, SimpleMode, Wallpaper


class SiteManager(admin.ModelAdmin):
    list_display = ['site_name','site_url','site_src','is_active']
    list_display_links = ['site_name']
    search_fields = ['site_name']


admin.site.register(Site, SiteManager)


class SimpleModeManager(admin.ModelAdmin):
    list_display = ['username','is_active']
    list_display_links = ['username']
    search_fields = ['username']


admin.site.register(SimpleMode, SimpleModeManager)


class WallpaperManager(admin.ModelAdmin):
    list_display = ['username', 'photo', 'photo_name', 'css']
    list_display_links = ['username']
    search_fields = ['username']


admin.site.register(Wallpaper, WallpaperManager)
