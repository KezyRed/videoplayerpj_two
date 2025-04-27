from django.shortcuts import render, get_object_or_404, redirect
from .models import Gallery, Video
from django.views.generic import ListView, DetailView
from .forms import CustomUserCreationForm


class GalleryListView(ListView):
    model = Gallery
    template_name = 'galleryvideo/gallery_list.html'
    context_object_name = 'galleries'
    ordering = ['-created_at']

class GalleryDetailView(DetailView):
    model = Gallery
    template_name = 'galleryvideo/gallery_detail.html'
    context_object_name = 'gallery'
    slug_url_kwarg = 'slug'

class VideoDetailView(DetailView):
    model = Video
    template_name = 'galleryvideo/video_detail.html'
    context_object_name = 'video'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gallery_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


