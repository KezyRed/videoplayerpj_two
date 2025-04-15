from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Gallery, Video

# Create your views here.
def index(request):
    videos = Video.objects.all()
    return render(request, 'galleryvideo/index.html', {'videos': videos})

def video_player(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'galleryvideo/video_player.html', {'video': video})