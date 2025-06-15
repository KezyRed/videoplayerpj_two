# videopj_two/galleryvideo/admin.py
from django.contrib import admin
from .models import Gallery, Video, Presentation, VideoTimecode

# Inline для видео в галерее
class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    fields = ('title_video_faculty', 'video_file', 'thumbnail')

# Inline для презентаций в видео
class PresentationInline(admin.TabularInline):
    model = Presentation
    extra = 1

# Inline для тайм-кодов в видео
class TimecodeInline(admin.TabularInline):
    model = VideoTimecode
    extra = 1
    fields = ('time_seconds', 'title', 'description', 'is_chapter')
    ordering = ['time_seconds']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [VideoInline]
    list_display = ('title_name_faculty', 'created_at')
    prepopulated_fields = {'slug_name_faculty': ('title_name_faculty',)}

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    inlines = [PresentationInline, TimecodeInline]
    list_display = ('title_video_faculty', 'gallery', 'get_timecodes_count', 'created_at')
    search_fields = ('title_video_faculty', 'description')
    list_filter = ('gallery', 'created_at')
    
    def get_timecodes_count(self, obj):
        return obj.timecodes.count()
    get_timecodes_count.short_description = 'Количество тайм-кодов'

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'video', 'uploaded_at')
    search_fields = ('title', 'video__title_video_faculty')
    list_filter = ('uploaded_at',)

@admin.register(VideoTimecode)
class TimecodeAdmin(admin.ModelAdmin):
    list_display = ('video', 'get_time_display', 'title', 'is_chapter', 'created_at')
    list_filter = ('is_chapter', 'video__gallery', 'created_at')
    search_fields = ('title', 'description', 'video__title_video_faculty')
    ordering = ['video', 'time_seconds']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('video', 'time_seconds', 'title', 'description')
        }),
        ('Дополнительные настройки', {
            'fields': ('is_chapter', 'thumbnail'),
            'classes': ('collapse',)
        }),
    )
    
    def get_time_display(self, obj):
        return obj.get_time_display()
    get_time_display.short_description = 'Время'