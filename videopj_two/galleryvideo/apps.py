from django.apps import AppConfig


class GalleryvideoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'galleryvideo'

    def ready(self):
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name='Преподаватель')
        Group.objects.get_or_create(name='Студенты')