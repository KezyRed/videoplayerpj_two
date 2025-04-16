from django.shortcuts import render, get_object_or_404
from .models import Gallery, Video
from django.views.generic import ListView, DetailView

# Create your views here.
# def gallery_list(request):
#     galleries = Gallery.objects.all().prefetch_related('videos')
#     print(f"DEBUG: Количество факультетов: {galleries.count()}")
#     return render(request, 'galleryvideo/gallery_list.html', {'galleries': galleries})

# def video_detail(request, id):
#     video = get_object_or_404(Video.objects.select_related('gallery'), id=id)
#     return render(request, 'galleryvideo/video_detail.html', {'video': video})

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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['gallery'] = self.object.gallery  # Добавляем объект галереи в контекст
    #     return context


