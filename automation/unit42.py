import os
import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_upload_app():
    project_name = "upload_project"
    app_name = "gallery"

    print("--- Unit-IV: File Upload Project Setup Start ---")
    
    if not os.path.exists(project_name):
        run_command(f"django-admin startproject {project_name}")
    
    os.chdir(project_name)
    run_command(f"python manage.py startapp {app_name}")

    # 1. Create Model with ImageField (models.py)
    with open(f"{app_name}/models.py", "w") as f:
        f.write("from django.db import models\n\nclass Photo(models.Model):\n    title = models.CharField(max_length=100)\n    image = models.ImageField(upload_to='pics/')\n\n    def __str__(self): return self.title")

    # 2. Create Form (forms.py)
    with open(f"{app_name}/forms.py", "w") as f:
        f.write("from django import forms\nfrom .models import Photo\n\nclass PhotoForm(forms.ModelForm):\n    class Meta:\n        model = Photo\n        fields = '__all__'")

    # 3. Create Views (views.py)
    views_code = f"""from django.shortcuts import render, redirect
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
    return render(request, '{app_name}/upload.html', {{'form': form}})

def display_view(request):
    photos = Photo.objects.all()
    return render(request, '{app_name}/display.html', {{'photos': photos}})
"""
    with open(f"{app_name}/views.py", "w") as f:
        f.write(views_code)

    # 4. App URLs (urls.py)
    with open(f"{app_name}/urls.py", "w") as f:
        f.write("from django.urls import path\nfrom . import views\nurlpatterns = [path('upload/', views.upload_view, name='upload'), path('display/', views.display_view, name='display')]")

    # 5. Templates
    t_dir = f"{app_name}/templates/{app_name}"
    os.makedirs(t_dir, exist_ok=True)
    with open(f"{t_dir}/upload.html", "w") as f:
        f.write("<h2>Upload Image</h2><form method='post' enctype='multipart/form-data'>{% csrf_token %}{{ form.as_p }}<button>Upload</button></form>")
    with open(f"{t_dir}/display.html", "w") as f:
        f.write("<h2>Gallery</h2>{% for p in photos %}<div><h3>{{ p.title }}</h3><img src='{{ p.image.url }}' width='200'></div>{% endfor %}")

    # 6. CRITICAL: Update settings.py for Media Files
    s_path = f"{project_name}/settings.py"
    with open(s_path, "a") as f:
        f.write("\nimport os\nMEDIA_URL = '/media/'\nMEDIA_ROOT = os.path.join(BASE_DIR, 'media/')\n")
    
    with open(s_path, "r") as f: s = f.read()
    if f"'{app_name}'" not in s:
        with open(s_path, "w") as f: f.write(s.replace("'django.contrib.staticfiles',", f"'django.contrib.staticfiles',\n    '{app_name}',"))

    # 7. Update Project urls.py (Serve Media)
    u_path = f"{project_name}/urls.py"
    u_code = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gallery.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""
    with open(u_path, "w") as f: f.write(u_code)

    # 8. Migrations (Pillow requirement notice)
    print("Checking for Pillow library...")
    run_command("pip install Pillow")
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")

    print(f"\nUPLOAD APP READY!\n1. cd {project_name}\n2. python manage.py runserver")

if __name__ == "__main__":
    setup_upload_app()