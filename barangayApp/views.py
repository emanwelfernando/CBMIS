from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import *
from .filters import *

def home_page(request):

    total_residents = Resident.objects.count()
    total_spots = TouristSpot.objects.count()
    total_households = Household.objects.count()
    spots = TouristSpot.objects.all()
    

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if request.user.is_superuser:
                return redirect('redirect-admin')
            elif user.user_type == 'super_admin':
                return redirect('super-admin-dashboard')
            elif user.user_type == 'provincial_admin':
                return redirect('provincial-admin-dashboard')
            elif user.user_type == 'municipal_admin':
                return redirect('municipal-admin-dashboard')
            elif user.user_type == 'municipal_staff':
                return redirect('municipal-staff-dashboard')
            elif user.user_type == 'barangay_admin':
                return redirect('barangay-admin-dashboard')
            elif user.user_type == 'barangay_staff':
                return redirect('barangay-staff-dashboard')
            elif user.user_type == 'tourist_staff':
                return redirect('tourist-staff-dashboard')
            else:
                # Handle other user types or display an error message
                return redirect('home-page')
        else:
            # Handle invalid credentials or display an error message
            return redirect('home-page')

    context = {
        'spots': spots, 
        'total_spots': total_spots,
        'total_residents': total_residents,
        'total_households': total_households,
    }

    return render(request, 'homePage/index.html', context)

def map_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Perform user type identification
            if request.user.is_superuser:
                return redirect('redirect-admin')
            elif user.user_type == 'super_admin':
                return redirect('super-admin-dashboard')
            elif user.user_type == 'provincial_admin':
                return redirect('provincial-admin-dashboard')
            elif user.user_type == 'municipal_admin':
                return redirect('municipal-admin-dashboard')
            elif user.user_type == 'municipal_staff':
                return redirect('municipal-staff-dashboard')
            elif user.user_type == 'barangay_admin':
                return redirect('barangay-admin-dashboard')
            elif user.user_type == 'barangay_staff':
                return redirect('barangay-staff-dashboard')
            elif user.user_type == 'tourist_staff':
                return redirect('tourist-staff-dashboard')
            else:
                # Handle other user types or display an error message
                return redirect('map-page')
        else:
            # Handle invalid credentials or display an error message
            return redirect('map-page')

    spots = TouristSpot.objects.all()
    Tourist_spotsFilter = Tourist_spotsFilters(request.GET, queryset=spots)
    spots = Tourist_spotsFilter.qs

    municipals = Municipal.objects.all()

    filtering = Tourist_spotsFilters()

    context = {
        'spots': spots, 
        'municipals': municipals,
        'filtering': filtering
    }
    return render(request, 'mapPage/index.html', context)


def tourist_spot_detail(request, id):
    spot = get_object_or_404(TouristSpot, id=id)
    return render(request, 'tourist_spots/tourist_spot_detail.html', {'spot': spot})

def add_tourist_spot(request):
    if request.method == 'POST':
        name = request.POST['name']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        location = f'POINT({longitude} {latitude})'
        tourist_spot = TouristSpot(name=name, location=location)
        tourist_spot.save()
        return redirect('tourist_spot_list')
    return render(request, 'tourist_spots/add_tourist_spot.html')

def edit_tourist_spot(request, id):
    spot = get_object_or_404(TouristSpot, id=id)
    if request.method == 'POST':
        spot.name = request.POST['name']
        spot.location = f'POINT({request.POST["longitude"]} {request.POST["latitude"]})'
        spot.save()
        return redirect('tourist_spot_list')
    return render(request, 'tourist_spots/edit_tourist_spot.html', {'spot': spot})

# def home_page(request):
#     return render(request, 'Basic/index.html')

def logoutUser(request):
    logout(request)
    return redirect('home-page')

def provincial_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None and user.user_type == 'provincial_admin':
            # Log in the user
            login(request, user)
            return redirect('provincial-admin-dashboard')  # Redirect to dashboard or any other page
            
        else:
            # If authentication fails, you can handle it here (e.g., display an error message)
            error_message = "Invalid credentials. Please try again."
            return render(request, 'homePage/home.html', {'error_message': error_message})
    
    return render(request, 'homePage/home.html')

