import os
import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_crud_app():
    project_name = "crud_project"
    app_name = "myapp"

    print("--- Unit-IV: CRUD Operations Project Setup Start ---")
    
    if not os.path.exists(project_name):
        run_command(f"django-admin startproject {project_name}")
    
    os.chdir(project_name)
    run_command(f"python manage.py startapp {app_name}")

    # 1. Create Model (models.py)
    with open(f"{app_name}/models.py", "w") as f:
        f.write("from django.db import models\n\nclass Student(models.Model):\n    name = models.CharField(max_length=100)\n    email = models.EmailField()\n    course = models.CharField(max_length=100)\n\n    def __str__(self): return self.name")

    # 2. Create Form (forms.py)
    with open(f"{app_name}/forms.py", "w") as f:
        f.write("from django import forms\nfrom .models import Student\n\nclass StudentForm(forms.ModelForm):\n    class Meta:\n        model = Student\n        fields = '__all__'")

    # 3. Create CRUD Views (views.py)
    views_code = f"""from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

def student_list(request):
    students = Student.objects.all()
    return render(request, '{app_name}/list.html', {{'students': students}})

def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, '{app_name}/form.html', {{'form': form}})

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, '{app_name}/form.html', {{'form': form}})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, '{app_name}/confirm_delete.html', {{'student': student}})
"""
    with open(f"{app_name}/views.py", "w") as f:
        f.write(views_code)

    # 4. App URLs (urls.py)
    urls_code = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('new/', views.student_create, name='student_create'),
    path('edit/<int:pk>/', views.student_update, name='student_update'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
]"""
    with open(f"{app_name}/urls.py", "w") as f:
        f.write(urls_code)

    # 5. Templates
    t_dir = f"{app_name}/templates/{app_name}"
    os.makedirs(t_dir, exist_ok=True)
    with open(f"{t_dir}/list.html", "w") as f:
        f.write("<h2>Students</h2><a href='{% url \"student_create\" %}'>Add New</a><table border='1'><tr><th>Name</th><th>Actions</th></tr>{% for s in students %}<tr><td>{{ s.name }}</td><td><a href='{% url \"student_update\" s.pk %}'>Edit</a> | <a href='{% url \"student_delete\" s.pk %}'>Delete</a></td></tr>{% endfor %}</table>")
    with open(f"{t_dir}/form.html", "w") as f:
        f.write("<h2>Student Form</h2><form method='post'>{% csrf_token %}{{ form.as_p }}<button>Save</button></form>")
    with open(f"{t_dir}/confirm_delete.html", "w") as f:
        f.write("<h2>Are you sure?</h2><form method='post'>{% csrf_token %}<button>Confirm Delete</button></form>")

    # 6. Update settings.py & Project urls.py
    s_path = f"{project_name}/settings.py"
    with open(s_path, "r") as f: s = f.read()
    if f"'{app_name}'" not in s:
        with open(s_path, "w") as f: f.write(s.replace("'django.contrib.staticfiles',", f"'django.contrib.staticfiles',\n    '{app_name}',"))

    with open(f"{project_name}/urls.py", "w") as f:
        f.write(f"from django.contrib import admin\nfrom django.urls import path, include\nurlpatterns = [path('admin/', admin.site.urls), path('', include('{app_name}.urls'))]")

    # 7. Migrations
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")

    print(f"\nCRUD APP READY!\n1. cd {project_name}\n2. python manage.py runserver")

if __name__ == "__main__":
    setup_crud_app()