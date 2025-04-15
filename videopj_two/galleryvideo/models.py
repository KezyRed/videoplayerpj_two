from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify


# Create your models here.
class Gallery(models.Model):
    title_name_faculty = models.CharField(max_length=50, verbose_name="Название галерее Видео уроков Факультета")
    slug_name_faculty = models.SlugField(max_length=50, unique=True)
    image_faculty = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title_name_faculty
    
    class Meta:
        verbose_name = "Название Факультета"
        verbose_name_plural = "Название Факультета"
        ordering = ['-created_at']


class Video(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True, blank=True,related_name='videos', verbose_name='Галерея видеоуроков')
    title_video_faculty = models.CharField(max_length=100, verbose_name="Название видиоурока")
    description = models.TextField(blank=True, verbose_name="Описание")
    video_file = models.FileField(upload_to='videos/', verbose_name="Видеофайл",validators=[FileExtensionValidator(['mp4', 'mov', 'avi'])])
    thumbnail = models.ImageField(upload_to='thumbnails/', verbose_name="Превью")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.title_video_faculty
    
    class Meta:
        verbose_name = "Видеоурок"
        verbose_name_plural = "Видеоуроки"
        ordering = ['-created_at']

class Presentation(models.Model):
    pass