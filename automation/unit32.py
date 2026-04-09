import os
import subprocess

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_sample_form():
    project_name = "form_project"
    app_name = "myapp"

    print("--- Unit-III: Sample Form Setup Start ---")
    
    if not os.path.exists(project_name):
        run_command(f"django-admin startproject {project_name}")
    
    os.chdir(project_name)
    run_command(f"python manage.py startapp {app_name}")

    # 1. Create Form (forms.py)
    forms_code = """from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
"""
    with open(f"{app_name}/forms.py", "w") as f:
        f.write(forms_code)

    # 2. Create Views (views.py)
    views_code = f"""from django.shortcuts import render
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return render(request, '{app_name}/success.html', {{'name': form.cleaned_data['name']}})
    else:
        form = ContactForm()
    return render(request, '{app_name}/contact.html', {{'form': form}})
"""
    with open(f"{app_name}/views.py", "w") as f:
        f.write(views_code)

    # 3. App URLs (urls.py)
    with open(f"{app_name}/urls.py", "w") as f:
        f.write("from django.urls import path\nfrom .views import contact_view\nurlpatterns = [path('contact/', contact_view)]")

    # 4. Templates
    t_dir = f"{app_name}/templates/{app_name}"
    os.makedirs(t_dir, exist_ok=True)
    with open(f"{t_dir}/contact.html", "w") as f:
        f.write("<h2>Contact Us</h2><form method='post'>{% csrf_token %}{{ form.as_p }}<button>Submit</button></form>")
    with open(f"{t_dir}/success.html", "w") as f:
        f.write("<h2>Thank you {{ name }}!</h2><p>Form submitted successfully.</p>")

    # 5. Settings & Main URLs
    s_path = f"{project_name}/settings.py"
    with open(s_path, "r") as f: s = f.read()
    if f"'{app_name}'" not in s:
        with open(s_path, "w") as f: f.write(s.replace("'django.contrib.staticfiles',", f"'django.contrib.staticfiles',\n    '{app_name}',"))

    with open(f"{project_name}/urls.py", "w") as f:
        f.write(f"from django.contrib import admin\nfrom django.urls import path, include\nurlpatterns = [path('admin/', admin.site.urls), path('', include('{app_name}.urls'))]")

    print(f"\nFAST TRACK SUCCESS!\n1. cd {project_name}\n2. python manage.py runserver")

if __name__ == "__main__":
    setup_sample_form()