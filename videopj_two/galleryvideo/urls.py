# videogallery/urls.py
from django.urls import path
from . import views

app_name = 'galleryvideo'  # Namespace для приложения

urlpatterns = [
    path('', views.index, name='index'),
    path('video/<int:video_id>/', views.video_player, name='video_player'),
]