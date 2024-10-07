from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import CustomUser, Agency, Profile, Destination, Accommodation, Booking
from .forms import ProfileForm
from django.conf import settings
from datetime import datetime, date
from weasyprint import HTML
from django.contrib.auth import get_user_model

User = get_user_model()  # This will return the custom user model

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        try:
            user = CustomUser.objects.create_user(email=email, username=username, password=password1)
            auth_login(request, user)
            return redirect('agencies_list')  
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect('signup')

    return render(request, 'pages/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(request, username=username, password1=password1)
        if user is not None:
            auth_login(request, user)
            if user.role == 'accommodation_receptionist':
                return redirect('accommodation_list')
            elif user.role == 'agency_receptionist':
                return redirect('agency_home')
            elif user.role == 'admin':
                return redirect('admin_home')
            else:
                return redirect('destination')
        else:
            messages.error(request, 'Wrong username or password')
        
    return render(request, 'pages/login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        roles = request.POST['roles']

        user = authenticate(request, username=username, password1=password1, roles=roles)
        
        if user is not None:
            login(request, user)
            return redirect('agency_home')  
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'pages/Admin/adminlogin.html')


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

# @login_required
# def receptionist_accommodations(request):
#     if not request.user.groups.filter(name='Accommodation Receptionist').exists():
#         return redirect('not_authorized')  # Redirect if the user is not a receptionist
#     # Proceed with rendering the page for receptionists
#     receptionist = get_object_or_404(Accommodation_Receptionist, user=request.user)
#     accommodations = receptionist.accommodations.all()
#     return render(request, 'receptionist/receptionist_accommodation_list.html', {'accommodations': accommodations})

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
#                    Admin View
###############################################################################################

#@user_passes_test(lambda u: u.is_superuser)  # Only allow access to superusers
def admin_home_view(request):
    total_users = CustomUser.objects.count()
    total_clients = CustomUser.objects.filter(roles='client').count()
    total_receptionists = CustomUser.objects.filter(roles='agency_receptionist').count()
    
    context = {
        'total_users': total_users,
        'total_clients': total_clients,
        'total_receptionists': total_receptionists,
    }

    users = CustomUser.objects.all()

    context = {
        'users': users,
    }

    return render(request, 'pages/Admin/adminhome.html', context)


#@login_required
#@user_passes_test(lambda u: u.is_superuser)
def create_receptionist_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('create_receptionist')

        try:
            user = CustomUser.objects.create_user(email=email, username=username, password=password1, roles='agency_receptionist')
            messages.success(request, f"Account created successfully.")
            return redirect('admin_home')  
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect('create_receptionist')

    return render(request, 'pages/Admin/createReceptionist.html')


def user_list_view(request):
    users = CustomUser.objects.all()
    
    # Group users by role
    grouped_users = {
        'admin': users.filter(roles='admin'),
        'accommodation_receptionist': users.filter(roles='accommodation_receptionist'),
        'agency_receptionist': users.filter(roles='agency_receptionist'),
        'client': users.filter(roles='client'),
    }

    context = {
        'grouped_users': grouped_users,
    }
    return render(request, 'admin_home.html', context)


#@user_passes_test(lambda u: u.is_superuser)
def delete_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User {user.email} has been deleted.')
        return redirect('admin_home') 
    context = {
        'user': user
    }
    return render(request, 'pages/Admin/deleteuser.html', context)


def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.roles = request.POST.get('roles')
        user.is_active = 'is_active' in request.POST  
        
        user.save()
        messages.success(request, f'User {user.username} has been updated successfully.')
        return redirect('admin_home')  

    context = {
        'user': user
    }
    return render(request, 'pages/Admin/edituser.html', context)


###############################################################################################
#                    Agency View
###############################################################################################


def agency_home_view(request):
    return render(request, 'pages/Agency/agencyhome.html')


#@user_passes_test(lambda u: u.is_superuser)
def create_agency_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        agency_receptionist_id = request.POST.get('agency_receptionist')
        
        if Agency.objects.filter(name=name).exists():
            messages.error(request, 'Agency with this name already exists!')
            return render(request, 'pages/Admin/createagency.html', {'receptionists': User.objects.filter(roles='agency_receptionist')})

        Agency.objects.create(
            name=name,
            description=description,
            image=image,
            agency_receptionist_id=agency_receptionist_id
        )
        messages.success(request, 'Agency created successfully!')
        return redirect('list_agencies') 
    
    receptionists = User.objects.filter(roles='agency_receptionist')

    return render(request, 'pages/Admin/createagency.html', {'receptionists': receptionists})

def list_agencies_view(request):
    agencies = Agency.objects.all() 
    context = {
        'agencies': agencies
    }
    return render(request, 'pages/Admin/list_agencies.html', context)

def list_agencies(request):
    agencies = Agency.objects.all() 
    context = {
        'agencies': agencies
    }
    return render(request, 'pages/UserDashboard/agency.html', context)



# def list_agencies_view(request):
#     agencies = Agency.objects.all() 
#     if request.user.roles == 'admin':
#         return render(request, 'pages/Admin/list_agencies.html', {'agencies': agencies})
#     else:
#         return render(request, 'pages/UserDashboard/agency.html', {'agencies': agencies})



#@user_passes_test(lambda u: u.is_superuser)
def update_agency_view(request, agency_id):
    agency = get_object_or_404(Agency, id=agency_id)
    
    if request.method == 'POST':
        agency.name = request.POST.get('name')
        agency.description = request.POST.get('description')
        
        # Check if an image was uploaded and update it
        if 'image' in request.FILES:
            agency.image = request.FILES['image']
        
        agency_receptionist_id = request.POST.get('agency_receptionist')
        if agency_receptionist_id:
            agency.agency_receptionist_id = agency_receptionist_id
        
        agency.save()
        messages.success(request, 'Agency updated successfully!')
        return redirect('list_agencies')

    # Fetch all users with the agency_receptionist role
    receptionists = User.objects.filter(roles='agency_receptionist')
    
    return render(request, 'pages/Admin/updateagency.html', {'agency': agency,'receptionists': receptionists})


def delete_agency_view(request, agency_id):
    agency = get_object_or_404(Agency, id=agency_id)
    
    if request.method == 'POST':  
        agency.delete()
        messages.success(request, 'Agency deleted successfully!')
        return redirect('list_agencies')

    return render(request, 'pages/Admin/deleteagency.html', {'agency': agency})


@login_required
def agency_receptionist(request):
    # Ensure the logged-in user is an agency receptionist
    if request.user.roles != 'agency_receptionist':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home') 
    
    agency = Agency.objects.filter(agency_receptionist=request.user).first()

    if not agency:
        messages.error(request, "No agency is assigned to you.")
        return redirect('home')  

    return render(request, 'pages/Agency/agencyreceptionist.html', {'agency': agency})





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
    return render(request, 'pages/UserDashboard/doualaStays.html', {'destination': destination})


###############################################################################################
#                    Accommodation and Booking View
###############################################################################################


def accommodation_list(request):
    accommodations = Accommodation.objects.all()
    return render(request, 'pages/UserDashboard/accommodation_list.html', {'accommodations': accommodations})

    # hotels = Accommodation.objects.filter(type_of_accommodation='Hotel')
    # apartments = Accommodation.objects.filter(type_of_accommodation='Apartment')
    # villas = Accommodation.objects.filter(type_of_accommodation='Villa')

    # return render(request, 'pages/UserDashboard/accommodation_list.html', {
    #     'hotels': hotels,
    #     'apartments': apartments,
    #     'villas': villas
    # })

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





# def agencies_list(request):
#     agencies = Agency.objects.all() 
#     return render(request, 'pages/UserDashboard/agency_list.html', {'agencies': agencies})






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





