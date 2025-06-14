from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone


# Create your models here.
class Gallery(models.Model):
    title_name_faculty = models.CharField(max_length=50, verbose_name="Название галерее Видео уроков Факультета")
    slug_name_faculty = models.SlugField(max_length=50, unique=True)
    image_faculty = models.ImageField(upload_to="images/", verbose_name="Изображение факультета")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title_name_faculty
    
    def get_absolute_url(self):
        return reverse('galleryvideo:gallery_detail', kwargs={'slug': self.slug_name_faculty})
    
    def save(self, *args, **kwargs):
        if not self.slug_name_faculty:
            self.slug_name_faculty = slugify(self.title_name_faculty)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Название Факультетов"
        verbose_name_plural = "Название Факультетов"
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
    
    def get_absolute_url(self):
        return reverse('galleryvideo:video_detail', args=[str(self.id)])
    
    class Meta:
        verbose_name = "Видеоурок"
        verbose_name_plural = "Видеоуроки"
        ordering = ['-created_at']



class Presentation(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='presentations', verbose_name='Видео')
    title = models.CharField(max_length=100, verbose_name="Название презентации")
    presentation_file = models.FileField(
        upload_to='presentations/', 
        verbose_name="Файл презентации",
        validators=[FileExtensionValidator(['odp', 'pptx', 'ppt'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Презентация"
        verbose_name_plural = "Презентации"
        ordering = ['title']