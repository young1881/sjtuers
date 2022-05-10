# Generated by Django 4.0.2 on 2022-05-10 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30, verbose_name='用户名')),
                ('jaccount', models.CharField(max_length=30, unique=True, verbose_name='Jaccount')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'User',
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Wallpaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='visitor', max_length=64)),
                ('photo', models.ImageField(default='#', upload_to='wallpaper/')),
                ('photo_name', models.CharField(default='visitor.jpg', max_length=120)),
                ('css', models.CharField(default='', max_length=120)),
                ('user', models.ForeignKey(default='000', on_delete=django.db.models.deletion.CASCADE, to='index.user', to_field='jaccount')),
            ],
            options={
                'verbose_name': 'Wallpaper',
                'verbose_name_plural': 'Wallpaper',
                'db_table': 'Wallpaper',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=30, verbose_name='网站名')),
                ('site_url', models.CharField(max_length=120, verbose_name='网址')),
                ('site_src', models.CharField(max_length=120, verbose_name='图标地址')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否活跃')),
                ('user', models.ForeignKey(default='000', on_delete=django.db.models.deletion.CASCADE, to='index.user', to_field='jaccount')),
            ],
            options={
                'verbose_name': 'site',
                'verbose_name_plural': 'site',
                'db_table': 'site',
            },
        ),
        migrations.CreateModel(
            name='SimpleMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='visitor', max_length=30, verbose_name='用户名')),
                ('is_active', models.BooleanField(default=False, verbose_name='是否活跃')),
                ('user', models.ForeignKey(default='000', on_delete=django.db.models.deletion.CASCADE, to='index.user', to_field='jaccount')),
            ],
            options={
                'verbose_name': 'simpleMode',
                'verbose_name_plural': 'simpleMode',
                'db_table': 'simpleMode',
            },
        ),
        migrations.CreateModel(
            name='Countdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='visitor', max_length=64)),
                ('date_name', models.CharField(default='元旦', max_length=64)),
                ('year', models.IntegerField(default=2023)),
                ('month', models.IntegerField(default=1)),
                ('day', models.IntegerField(default=1)),
                ('user', models.ForeignKey(default='000', on_delete=django.db.models.deletion.CASCADE, to='index.user', to_field='jaccount')),
            ],
            options={
                'verbose_name': 'countdown',
                'verbose_name_plural': 'countdown',
                'db_table': 'countdown',
            },
        ),
    ]
