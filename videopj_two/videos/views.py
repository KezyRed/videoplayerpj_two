from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Video

# Create your views here.
class VideoListView(ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'
    ordering = ['-created_at']

class VideoDetailView(DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'