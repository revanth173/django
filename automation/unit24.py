import os
import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_tables_grids():
    project_name = "tablegrid_project"
    app_name = "myapp"

    print("--- Django Tables & Grids Project Setup Start Avthondi... ---")
    
    # 1. Project & App Creation
    run_command(f"django-admin startproject {project_name}")
    os.chdir(project_name)
    run_command(f"python manage.py startapp {app_name}")

    # 2. Define Employee Model (models.py)
    models_code = """from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField()

    def __str__(self):
        return self.name
"""
    with open(f"{app_name}/models.py", "w") as f:
        f.write(models_code)

    # 3. Create View to fetch data (views.py)
    views_code = f"""from django.shortcuts import render
from .models import Employee

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, '{app_name}/employee_list.html', {{'employees': employees}})
"""
    with open(f"{app_name}/views.py", "w") as f:
        f.write(views_code)

    # 4. Configure App URLs (urls.py)
    app_urls_code = """from django.urls import path
from .views import employee_list

urlpatterns = [
    path('', employee_list, name='employee_list'),
]"""
    with open(f"{app_name}/urls.py", "w") as f:
        f.write(app_urls_code)

    # 5. Create Template with Bootstrap Table & Grid
    template_dir = f"{app_name}/templates/{app_name}"
    os.makedirs(template_dir, exist_ok=True)
    
    html_content = """<!DOCTYPE html>
<html lang='en'><head>
  <meta charset='UTF-8'><title>Employee List</title>
  <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'>
</head><body>
<div class='container mt-4'>
  <h2 class='mb-3'>Employee List (Table)</h2>
  <table class='table table-bordered table-striped'>
    <thead class='table-dark'>
      <tr><th>Name</th><th>Department</th><th>Salary</th><th>Hire Date</th></tr>
    </thead><tbody>
    {% for employee in employees %}
    <tr>
      <td>{{ employee.name }}</td><td>{{ employee.department }}</td>
      <td>${{ employee.salary }}</td><td>{{ employee.hire_date }}</td>
    </tr>
    {% empty %}
    <tr><td colspan="4" class="text-center">No data found. Please add from Admin.</td></tr>
    {% endfor %}
    </tbody></table>

  <h2 class='mt-5'>Employee Grid (Cards)</h2>
  <div class='row'>
    {% for employee in employees %}
    <div class='col-md-4 mb-3'><div class='card p-3 shadow-sm'>
      <h5>{{ employee.name }}</h5>
      <p class='text-muted'>{{ employee.department }}</p>
      <p><strong>Salary:</strong> ${{ employee.salary }}</p>
    </div></div>
    {% endfor %}
  </div>
</div></body></html>"""
    
    with open(f"{template_dir}/employee_list.html", "w") as f:
        f.write(html_content)

    # 6. Update settings.py
    settings_file = f"{project_name}/settings.py"
    with open(settings_file, "r") as f:
        settings = f.read()
    with open(settings_file, "w") as f:
        f.write(settings.replace("'django.contrib.staticfiles',", f"'django.contrib.staticfiles',\n    '{app_name}',"))

    # 7. Update Project urls.py
    project_urls_code = f"""from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('{app_name}.urls')),
]"""
    with open(f"{project_name}/urls.py", "w") as f:
        f.write(project_urls_code)

    # 8. Database Migrations
    print("--- Database migrations run avthunnai... ---")
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")

    print(f"\n--- SUCCESS! ---")
    print(f"1. cd {project_name}")
    print(f"2. python manage.py runserver")

if __name__ == "__main__":
    setup_tables_grids()