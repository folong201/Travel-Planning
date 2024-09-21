from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Profile, Destination, Accommodation, Booking, Agency
from .forms import ProfileForm
from datetime import datetime, date
from weasyprint import HTML


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
            messages.error(request, 'Wrong username or password')
        
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


###############################################################################################
#                    Destination View
###############################################################################################


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

def destination_list(request):
    query = request.GET.get('q')  
    if query:
        destinations = Destination.objects.filter(name__icontains=query) | Destination.objects.filter(city__icontains=query) 
    else:
        destinations = Destination.objects.all()
    
    return render(request, 'pages/UserDashboard/destination.html', {'destinations': destinations, 'query': query})

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    return render(request, 'destination/destination_detail.html', {'destination': destination})


###############################################################################################
#                    Accommodation and Booking View
###############################################################################################


def accommodation_list(request):
    hotels = Accommodation.objects.filter(type_of_accommodation='Hotel')
    apartments = Accommodation.objects.filter(type_of_accommodation='Apartment')
    villas = Accommodation.objects.filter(type_of_accommodation='Villa')

    return render(request, 'pages/UserDashboard/accommodation_list.html', {
        'hotels': hotels,
        'apartments': apartments,
        'villas': villas
    })
def accommodation_detail(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)

    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        # Convert string dates to datetime.date objects
        if check_in_date and check_out_date:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()

            if check_in_date < date.today():
                messages.error(request, "Check-in date cannot be in the past.")
            elif check_out_date <= check_in_date:
                messages.error(request, "Check-out date must be after the check-in date.")
            else:
                nights = (check_out_date - check_in_date).days
                total_price = accommodation.price_per_night * nights

                booking = Booking.objects.create(
                    user=request.user,
                    accommodation=accommodation,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    total_price=total_price
                )

                return redirect('booking_detail', pk=booking.pk)
        else:
            messages.error(request, "Please select valid check-in and check-out dates.")

    return render(request, 'pages/UserDashboard/accommodation_detail.html', {'accommodation': accommodation})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'pages/UserDashboard/booking_detail.html', {'booking': booking})

def generate_eticket(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Render the HTML template with the booking details
    html_string = render_to_string('pages/UserDashboard/eticket.html', {'booking': booking})

    # Create an HttpResponse object and set the content type to application/pdf
    response = HttpResponse(content_type='application/pdf')

    # Set the file name for the downloaded PDF
    response['Content-Disposition'] = f'attachment; filename="e-ticket-{booking.id}.pdf"'

    # Convert the HTML string to PDF using WeasyPrint
    HTML(string=html_string).write_pdf(response)

    return response

###############################################################################################
#                    Agency View
###############################################################################################


def agencies_list(request):
    agencies = Agency.objects.all() 
    return render(request, 'pages/UserDashboard/agency_list.html', {'agencies': agencies})






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





