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
    fields = ('time_seconds', 'title', 'description', 'is_chapter', 'thumbnail')
    ordering = ['time_seconds']
    readonly_fields = ('get_time_display',)
    
    def get_time_display(self, obj):
        if obj.pk:
            return obj.get_time_display()
        return ""
    get_time_display.short_description = 'Время (ЧЧ:ММ:СС)'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [VideoInline]
    list_display = ('title_name_faculty', 'get_videos_count', 'created_at')
    prepopulated_fields = {'slug_name_faculty': ('title_name_faculty',)}
    search_fields = ('title_name_faculty',)
    
    def get_videos_count(self, obj):
        return obj.videos.count()
    get_videos_count.short_description = 'Количество видео'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    inlines = [PresentationInline, TimecodeInline]
    list_display = ('title_video_faculty', 'gallery', 'get_timecodes_count', 'get_chapters_count', 'created_at')
    search_fields = ('title_video_faculty', 'description')
    list_filter = ('gallery', 'created_at')
    readonly_fields = ('get_duration_info',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('gallery', 'title_video_faculty', 'description')
        }),
        ('Файлы', {
            'fields': ('video_file', 'thumbnail')
        }),
        ('Дополнительная информация', {
            'fields': ('get_duration_info',),
            'classes': ('collapse',)
        }),
    )
    
    def get_timecodes_count(self, obj):
        return obj.timecodes.count()
    get_timecodes_count.short_description = 'Всего таймкодов'
    
    def get_chapters_count(self, obj):
        return obj.timecodes.filter(is_chapter=True).count()
    get_chapters_count.short_description = 'Глав'
    
    def get_duration_info(self, obj):
        if obj.timecodes.exists():
            last_timecode = obj.timecodes.order_by('-time_seconds').first()
            return f"Последний таймкод: {last_timecode.get_time_display()}"
        return "Таймкоды не добавлены"
    get_duration_info.short_description = 'Информация о длительности'

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'video', 'uploaded_at')
    search_fields = ('title', 'video__title_video_faculty')
    list_filter = ('uploaded_at', 'video__gallery')

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
        ('Навигация', {
            'fields': ('get_navigation_info',),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ('get_navigation_info',)
    
    def get_time_display(self, obj):
        return obj.get_time_display()
    get_time_display.short_description = 'Время'
    
    def get_navigation_info(self, obj):
        if obj.pk:
            info = []
            prev_tc = obj.get_previous_timecode()
            next_tc = obj.get_next_timecode()
            
            if prev_tc:
                info.append(f"Предыдущий: {prev_tc.title} ({prev_tc.get_time_display()})")
            else:
                info.append("Предыдущий: отсутствует")
                
            if next_tc:
                info.append(f"Следующий: {next_tc.title} ({next_tc.get_time_display()})")
            else:
                info.append("Следующий: отсутствует")
                
            return " | ".join(info)
        return "Сохраните таймкод для просмотра навигации"
    get_navigation_info.short_description = 'Навигация'

# Дополнительные настройки админ-панели
admin.site.site_header = "Управление видеоуроками"
admin.site.site_title = "Видеоплеер МУИВ"
admin.site.index_title = "Панель управления контентом"