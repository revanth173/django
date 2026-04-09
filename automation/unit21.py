import os
import subprocess
import sys

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_hello_world():
    project_name = "helloworld_project"
    app_name = "myapp"

    print("--- Django Project Create chesthunna... ---")
    # 1. Create Django Project
    run_command(f"django-admin startproject {project_name}")
    os.chdir(project_name)

    # 2. Create Django App
    run_command(f"python manage.py startapp {app_name}")

    print("--- Files Update chesthunna... ---")
    
    # 3. [span_0](start_span)Update myapp/views.py[span_0](end_span)
    views_code = """from django.http import HttpResponse\n\ndef hello_world(request):\n    return HttpResponse("Hello, World!")"""
    with open(f"{app_name}/views.py", "w") as f:
        f.write(views_code)

    # 4. [span_1](start_span)Create myapp/urls.py[span_1](end_span)
    app_urls = """from django.urls import path\nfrom .views import hello_world\n\nurlpatterns = [\n    path('', hello_world, name='hello_world'),\n]"""
    with open(f"{app_name}/urls.py", "w") as f:
        f.write(app_urls)

    # 5. [span_2](start_span)Update Project settings.py (Add App)[span_2](end_span)
    settings_path = f"{project_name}/settings.py"
    with open(settings_path, "r") as f:
        settings = f.read()
    
    updated_settings = settings.replace(
        "'django.contrib.staticfiles',",
        f"'django.contrib.staticfiles',\n    '{app_name}',"
    )
    with open(settings_path, "w") as f:
        f.write(updated_settings)

    # 6. [span_3](start_span)Update Project urls.py (Include App URLs)[span_3](end_span)
    project_urls_path = f"{project_name}/urls.py"
    project_urls = """from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]"""
    with open(project_urls_path, "w") as f:
        f.write(project_urls)

    print(f"\n--- SUCCESS! ---")
    print(f"Ippudu terminal lo: cd {project_name}")
    print(f"Tarvatha: python manage.py runserver")

if __name__ == "__main__":
    setup_hello_world()