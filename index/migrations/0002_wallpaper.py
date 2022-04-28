# Generated by Django 4.0.2 on 2022-04-28 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallpaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='visitor', max_length=64)),
                ('photo', models.ImageField(upload_to='wallpaper/')),
                ('photo_name', models.CharField(default='visitor.jpg', max_length=120)),
            ],
            options={
                'verbose_name': 'Wallpaper',
                'verbose_name_plural': 'Wallpaper',
                'db_table': 'Wallpaper',
            },
        ),
    ]
