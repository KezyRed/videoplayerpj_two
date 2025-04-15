from django.urls import path
from . import views

urlpatterns = [
    path('', views.VideoListView.as_view(), name='video_list'),
    path('video/<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
]
