from django.shortcuts import render, redirect
from .forms import PhotoForm
from .models import Photo

def upload_view(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('display')
    else:
        form = PhotoForm()
    return render(request, 'gallery/upload.html', {'form': form})

def display_view(request):
    photos = Photo.objects.all()
    return render(request, 'gallery/display.html', {'photos': photos})
