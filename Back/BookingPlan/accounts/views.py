from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('destination')
    return render(request, 'pages/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('destination')
        else:
            return render(request, 'pages/login.html', {'error': 'Wrong username or password'})
    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'index.html')

def dashboard_view(request):
    return render(request, 'pages/UserDashboard/destination.html')

def agency_view(request):
    return render(request, 'pages/UserDashboard/agency.html')

def stays_view(request):
    return render(request, 'pages/UserDashboard/stays.html')

def schedule_view(request):
    return render(request, 'pages/UserDashboard/schedule.html')

def tips_view(request):
    return render(request, 'pages/UserDashboard/tips.html')

def base_view(request):
    return render(request, 'pages/UserDashboard/base.html')


