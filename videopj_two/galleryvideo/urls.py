# videogallery/urls.py
from django.urls import path
from . import views

app_name = 'galleryvideo'  # Namespace для приложения

urlpatterns = [
    path('', views.gallery_list, name='gallery_list'),
    path('video/<int:id>/', views.video_detail, name='video_detail'),
]