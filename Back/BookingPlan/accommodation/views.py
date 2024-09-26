from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Receptionist
from django.contrib import messages
from accounts.models import Accommodation

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accommodation_list')
        else:
            messages.error(request, 'Wrong username or password')
        
    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'index.html')


@login_required
def receptionist_accommodations(request):
    receptionist = get_object_or_404(Receptionist, user=request.user)
    accommodations = receptionist.accommodations.all()  # Only accommodations assigned to the logged-in receptionist
    return render(request, 'pages/Accommodation/accommodation_list.html', {'accommodations': accommodations})

@login_required
def receptionist_accommodation_detail(request, pk):
    receptionist = get_object_or_404(Receptionist, user=request.user)
    accommodation = get_object_or_404(receptionist.accommodations, pk=pk)  # Get accommodation assigned to this receptionist
    return render(request, 'pages/Accommodation/accommodation_detail.html', {'accommodation': accommodation})


def list_accommodations(request):
    accommodations = Accommodation.objects.all()
    return render(request, 'pages/UserDashboard/accommodation_list.html', {'accommodations': accommodations})

def accommodation_detail(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    return render(request, 'pages/UserDashboard/accommodation_detail.html', {'accommodation': accommodation})



