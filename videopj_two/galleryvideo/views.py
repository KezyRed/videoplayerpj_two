from django.shortcuts import render, get_object_or_404
from .models import Gallery, Video

# Create your views here.
def gallery_list(request):
    galleries = Gallery.objects.all()
    return render(request, 'galleryvideo/gallery_list.html', {'galleries': galleries})

def video_detail(request, id):
    video = get_object_or_404(Video, id=id)
    return render(request, 'galleryvideo/video_detail.html', {'video': video})