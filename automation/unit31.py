import os
import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_auth_registration():
    project_name = "reg_project"
    app_name = "authe"

    print("--- Unit-III: Registration Auth Project Setup ---")
    
    # 1. Project & App Creation
    if not os.path.exists(project_name):
        run_command(f"django-admin startproject {project_name}")
    
    os.chdir(project_name)
    run_command(f"python manage.py startapp {app_name}")

    # 2. Create User Registration Form (forms.py)
    forms_code = """from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
"""
    with open(f"{app_name}/forms.py", "w") as f:
        f.write(forms_code)

    # 3. Create Views (views.py)
    views_code = f"""from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, '{app_name}/register.html', {{'form': form}})

def home(request):
    return render(request, '{app_name}/home.html')
"""
    with open(f"{app_name}/views.py", "w") as f:
        f.write(views_code)

    # 4. Configure App URLs (urls.py)
    app_urls = """from django.urls import path
from .views import register, home

urlpatterns = [
    path('register/', register, name='register'),
    path('home/', home, name='home'),
]"""
    with open(f"{app_name}/urls.py", "w") as f:
        f.write(app_urls)

    # 5. Create Templates
    template_dir = f"{app_name}/templates/{app_name}"
    os.makedirs(template_dir, exist_ok=True)
    
    with open(f"{template_dir}/register.html", "w") as f:
        f.write("<h2>Register</h2><form method='post'>{% csrf_token %}{{ form.as_p }}<button type='submit'>Register</button></form>")
    
    with open(f"{template_dir}/home.html", "w") as f:
        f.write("<h2>Welcome!</h2><p>Registration Successful.</p>")

    # 6. Update settings.py (REFIXED)
    settings_file = f"{project_name}/settings.py"
    with open(settings_file, "r") as f:
        settings = f.read()
    
    if f"'{app_name}'" not in settings:
        updated_settings = settings.replace(
            "'django.contrib.staticfiles',",
            f"'django.contrib.staticfiles',\n    '{app_name}',"
        )
        with open(settings_file, "w") as f:
            f.write(updated_settings)

    # 7. Update Project urls.py
    project_urls = f"""from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('{app_name}.urls')),
]"""
    with open(f"{project_name}/urls.py", "w") as f:
        f.write(project_urls)

    # 8. Database Migrations
    print("Migrations running...")
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")

    print(f"\nSUCCESS! Ippudu: \n1. cd {project_name}\n2. python manage.py runserver")

if __name__ == "__main__":
    setup_auth_registration()