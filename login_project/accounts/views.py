from django.shortcuts import render, redirect
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
