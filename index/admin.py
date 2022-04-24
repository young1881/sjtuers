from django.contrib import admin

# Register your models here.
from .models import Site


class SiteManager(admin.ModelAdmin):
    list_display = ['site_name','site_url','site_src','is_active']
    list_display_links = ['site_name']
    search_fields = ['site_name']


admin.site.register(Site, SiteManager)