from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone


# Create your models here.
class Gallery(models.Model):
    title_name_faculty = models.CharField(max_length=50, verbose_name="Название галерее Видео-уроков")
    slug_name_faculty = models.SlugField(max_length=50, unique=True)
    image_faculty = models.ImageField(upload_to="images/", verbose_name="Изображение Видео-уроков")
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
        verbose_name = "Наименование Карточки темы"
        verbose_name_plural = "Наименование Карточки темы"
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
    
    def get_timecodes_json(self):
        '''возвращает тайм-код в формате JSON для video.js'''
        import json
        timecodes = []
        for tc in self.timecodes.all().order_by('time_seconds'):
            timecodes.append({
                'time': tc.time_seconds,
                'text':tc.title,
                'description':tc.description,
            })
        return timecodes
    
    def get_chapters(self):
        '''Возвращает только таймкоды, помеченные как главы'''
        return self.timecodes.filter(is_chapter=True).order_by('time_seconds')
    
    def get_all_timecodes(self):
        '''Возвращает все таймкоды, отсортированные по времени'''
        return self.timecodes.all().order_by('time_seconds')
    

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
        validators=[FileExtensionValidator(['odp', 'pptx', 'ppt', 'pdf'])]  # Ограничиваем типы файлов
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Презентация"
        verbose_name_plural = "Презентации"
        ordering = ['title']


class VideoTimecode(models.Model):
    """Модель для тайм-кодов видео"""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='timecodes', verbose_name='Видео')
    time_seconds = models.PositiveIntegerField(verbose_name='Время в секундах')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    # Дополнительные поля для улучшенной функциональности
    is_chapter = models.BooleanField(default=False, verbose_name='Это глава?', 
                                   help_text='Отметьте если это начало новой главы/раздела')
    thumbnail = models.ImageField(upload_to='timecode_thumbnails/', blank=True, null=True,
                                verbose_name='Миниатюра для тайм-кода')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def str(self):
        return f"{self.video.title_video_faculty} - {self.get_time_display()} - {self.title}"
    
    def get_time_display(self):
        """Преобразует секунды в формат ММ:СС или ЧЧ:ММ:СС"""
        hours = self.time_seconds // 3600
        minutes = (self.time_seconds % 3600) // 60
        seconds = self.time_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def save(self, *args, **kwargs):
        # Проверяем что время не превышает длительность видео (если известна)
        super().save(*args, **kwargs)
    
    def get_next_timecode(self):
        """Возвращает следующий таймкод"""
        return self.video.timecodes.filter(
            time_seconds__gt=self.time_seconds
        ).order_by('time_seconds').first()
    
    def get_previous_timecode(self):
        """Возвращает предыдущий таймкод"""
        return self.video.timecodes.filter(
            time_seconds__lt=self.time_seconds
        ).order_by('-time_seconds').first()
    
    
    class Meta:
        verbose_name = "Тайм-код"
        verbose_name_plural = "Тайм-коды"
        ordering = ['video', 'time_seconds']
        unique_together = ['video', 'time_seconds']  # Уникальность времени для каждого видео