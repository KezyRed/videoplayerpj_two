# Generated by Django 5.2 on 2025-06-14 23:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleryvideo', '0005_alter_gallery_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoTimecode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_seconds', models.PositiveIntegerField(verbose_name='Время в секундах')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('is_chapter', models.BooleanField(default=False, help_text='Отметьте если это начало новой главы/раздела', verbose_name='Это глава?')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='timecode_thumbnails/', verbose_name='Миниатюра для тайм-кода')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timecodes', to='galleryvideo.video', verbose_name='Видео')),
            ],
            options={
                'verbose_name': 'Тайм-код',
                'verbose_name_plural': 'Тайм-коды',
                'ordering': ['video', 'time_seconds'],
                'unique_together': {('video', 'time_seconds')},
            },
        ),
    ]
