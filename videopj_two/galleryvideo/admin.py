from django.contrib import admin
from .models import Gallery, Video

# Register your models here.
class Videoinline(admin.TabularInline):
    model = Video
    extra = 1

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [Videoinline]
    list_display = ('title_name_faculty','created_at')
    prepopulated_fields = {'slug_name_faculty': ('title_name_faculty',)}

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title_video_faculty', 'created_at')
    search_fields = ('title_video_faculty', 'description')
    list_filter = ('gallery','created_at',)