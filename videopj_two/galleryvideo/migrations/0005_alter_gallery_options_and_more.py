# Generated by Django 5.2 on 2025-04-27 16:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleryvideo', '0004_auto_20250425_2021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gallery',
            options={'ordering': ['-created_at'], 'verbose_name': 'Название Факультетов', 'verbose_name_plural': 'Название Факультетов'},
        ),
        migrations.AlterField(
            model_name='presentation',
            name='presentation_file',
            field=models.FileField(upload_to='presentations/', validators=[django.core.validators.FileExtensionValidator(['odp', 'pptx', 'ppt'])], verbose_name='Файл презентации'),
        ),
    ]
