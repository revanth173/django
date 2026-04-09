import os
import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_bootstrap_demo():
    project_name = "bootstrap_project"
    app_name = "bs"

    print("--- Django Bootstrap Project Setup Start Avthondi... ---")
    
    # 1. [span_1](start_span)Project & App Creation[span_1](end_span)
    run_command(f"django-admin startproject {project_name}")
    os.chdir(project_name)
    run_command(f"python manage.py startapp {app_name}")

    # 2. [span_2](start_span)Update bs/views.py[span_2](end_span)
    views_code = "from django.shortcuts import render\n\ndef home(request):\n    return render(request, 'home.html')"
    with open(f"{app_name}/views.py", "w") as f:
        f.write(views_code)

    # 3. [span_3](start_span)Create Template folder and home.html with Bootstrap CDN[span_3](end_span)
    template_path = f"{app_name}/templates"
    os.makedirs(template_path, exist_ok=True)
    
    bootstrap_html = """<!DOCTYPE html>
<html lang='en'><head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>Django with Bootstrap</title>
  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
</head><body>
  <nav class='navbar navbar-expand-lg navbar-dark bg-dark'>
    <div class='container'>
      <a class='navbar-brand' href='#'>My Django App</a>
    </div>
  </nav>
  <div class='container mt-5'>
    <div class='row'>
      <div class='col-md-8 offset-md-2 text-center'>
        <h1>Welcome to Django with Bootstrap</h1>
        <p class='lead'>Bootstrap integration demo.</p>
        <a href='#' class='btn btn-primary'>Learn More</a>
      </div>
    </div>
  </div>
  <footer class='bg-dark text-white text-center py-3 mt-5'>
    &copy; 2026 My Django App
  </footer>
  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>
</body></html>"""
    
    with open(f"{template_path}/home.html", "w") as f:
        f.write(bootstrap_html)

    # 4. [span_4](start_span)Update settings.py (INSTALLED_APPS)[span_4](end_span)
    settings_file = f"{project_name}/settings.py"
    with open(settings_file, "r") as f:
        settings = f.read()
    with open(settings_file, "w") as f:
        f.write(settings.replace("'django.contrib.staticfiles',", f"'django.contrib.staticfiles',\n    '{app_name}',"))

    # 5. [span_5](start_span)Update Project urls.py[span_5](end_span)
    project_urls_code = f"""from django.contrib import admin
from django.urls import path
from {app_name}.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]"""
    with open(f"{project_name}/urls.py", "w") as f:
        f.write(project_urls_code)

    print(f"\n--- SUCCESS! ---")
    print(f"1. cd {project_name}")
    print(f"2. python manage.py runserver")

if __name__ == "__main__":
    setup_bootstrap_demo()