# videogallery/urls.py
from django.urls import path
from . import views

app_name = 'galleryvideo'  # Namespace для приложения

urlpatterns = [
    path('', views.GalleryListView.as_view(), name='gallery_list'),
    path('gallery/<slug:slug>/', views.GalleryListView.as_view(), name='gallery_detail'),  # Изменено на slug
    path('video/<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
    # path('gallery/<int:pk>/', views.GalleryDetailView.as_view(), name='gallery_detail'),  # Если нужно
    
]