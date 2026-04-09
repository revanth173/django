import os
import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_mvc_login():
    project_name = "login_project"
    app_name = "accounts"

    print("--- MVC Login Project Create chesthunna... ---")
    # 1. Create Django Project & App
    run_command(f"django-admin startproject {project_name}")
    os.chdir(project_name)
    run_command(f"python manage.py startapp {app_name}")

    # 2. [span_4](start_span)Update accounts/views.py (MVC Logic)[span_4](end_span)
    views_code = """from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def register(request):
    if request.method == "POST":
        u = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        user = User.objects.create_user(username=u, email=e, password=p)
        user.save()
        messages.success(request, "Registration successful")
        return redirect('login')
    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return render(request, 'accounts/dashboard.html')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')
"""
    with open(f"{app_name}/views.py", "w") as f:
        f.write(views_code)

    # 3. [span_5](start_span)Create accounts/urls.py[span_5](end_span)
    app_urls = """from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]"""
    with open(f"{app_name}/urls.py", "w") as f:
        f.write(app_urls)

    # 4. [span_6](start_span)[span_7](start_span)Create Templates[span_6](end_span)[span_7](end_span)
    template_path = f"{app_name}/templates/accounts"
    os.makedirs(template_path, exist_ok=True)
    
    with open(f"{template_path}/login.html", "w") as f:
        f.write("<h2>Login</h2><form method='POST'>{% csrf_token %}<input name='username' placeholder='Username' required><br><input type='password' name='password' placeholder='Password' required><br><button type='submit'>Login</button></form><a href='{% url \"register\" %}'>Create account</a>")
    
    with open(f"{template_path}/register.html", "w") as f:
        f.write("<h2>Register</h2><form method='POST'>{% csrf_token %}<input name='username' placeholder='Username' required><br><input name='email' placeholder='Email' required><br><input type='password' name='password' placeholder='Password' required><br><button type='submit'>Register</button></form><a href='{% url \"login\" %}'>Login here</a>")

    with open(f"{template_path}/dashboard.html", "w") as f:
        f.write("<h2>Welcome to Dashboard!</h2><p>Login Successful.</p>")

    # 5. [span_8](start_span)[span_9](start_span)Update settings.py & Project urls.py[span_8](end_span)[span_9](end_span)
    settings_path = f"{project_name}/settings.py"
    with open(settings_path, "r") as f:
        settings = f.read()
    with open(settings_path, "w") as f:
        f.write(settings.replace("'django.contrib.staticfiles',", f"'django.contrib.staticfiles',\n    '{app_name}',"))

    with open(f"{project_name}/urls.py", "w") as f:
        f.write("from django.contrib import admin\nfrom django.urls import path, include\n\nurlpatterns = [\n    path('admin/', admin.site.urls),\n    path('accounts/', include('accounts.urls')),\n]")

    # 6. [span_10](start_span)Run Migrations[span_10](end_span)
    run_command("python manage.py migrate")

    print(f"--- SUCCESS! ---\n1. cd {project_name}\n2. python manage.py runserver")

if __name__ == "__main__":
    setup_mvc_login()