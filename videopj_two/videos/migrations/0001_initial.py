# Generated by Django 5.1.4 on 2025-04-15 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('video_file', models.FileField(upload_to='videos/')),
                ('thumbnail', models.ImageField(blank=True, upload_to='thumbnails/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
