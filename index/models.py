from django.db import models


class Site(models.Model):
    site_name = models.CharField('网站名', max_length=30)
    site_url = models.CharField('网址', max_length=120)
    site_src = models.CharField('图标地址', max_length=120)
    is_active = models.BooleanField('是否活跃', default=True)

    class Meta:
        db_table = 'site'
        verbose_name = 'site'
        verbose_name_plural = 'site'

    def __str__(self):
        return '网址 %s'%(self.site_name)