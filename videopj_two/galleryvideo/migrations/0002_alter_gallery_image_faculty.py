# Generated by Django 5.1.4 on 2025-04-16 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleryvideo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image_faculty',
            field=models.ImageField(upload_to='images/', verbose_name='Изображение факультета'),
        ),
    ]
