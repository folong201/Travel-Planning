from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Destination
from .forms import ProfileForm


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
            return redirect('create_profile')
        else:
            messages.error(request, 'pages/login.html', {'error': 'Wrong username or password'})
        
    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'index.html')

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  
            profile.save()
            return redirect('destination')
    else:
        form = ProfileForm()
    
    return render(request, 'pages/editProfile.html', {'form': form})

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'post':
        form = ProfileForm(request.POST, request.Files, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('destination')
        else:
            form = ProfileForm(instance=profile)

        return render(request, 'pages/editProfile.html', {'form': form})

def create_destination(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        city = request.POST.get('city')
        popular_attractions = request.POST.get('popular_attractions')
        image = request.FILES.get('image') 
        
        if name and popular_attractions and image:
            destination = Destination(
                name=name,
                description=description,
                city=city,
                popular_attractions=popular_attractions,
                image=image
            )
            destination.save()
            messages.success(request, "Destination created successfully!")
            return redirect('pages/destination')
        else:
            messages.error(request, "Please fill in all the required fields.")
    
    return render(request, 'destination/create_destination.html')



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





