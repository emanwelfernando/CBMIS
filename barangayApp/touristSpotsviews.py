
from .models import TouristSpot
from .filters import *

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Count
from django.db.models import Avg
from django.db.models.functions import Round
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from auditlog.models import LogEntry as AuditLogEntry
from auditlog.models import LogEntry

import json

@login_required
@permission_required('barangayApp.can_view_tourist_staff_views', raise_exception=True)
def dashboard(request):
    user = request.user

    municipal = user.municipal
    
    if not municipal:
        return HttpResponse("You are not associated with any municipal.")
    
    most_common_spot_type = TouristSpot.objects.filter(municipal=municipal) \
        .values('spot_type') \
        .annotate(count=Count('spot_type')) \
        .order_by('-count') \
        .first()

    spot_type_counts = TouristSpot.objects.filter(municipal=municipal) \
        .values('spot_type') \
        .annotate(count=Count('spot_type')) \
        .order_by('-count')

    spot_types = [entry['spot_type'] for entry in spot_type_counts]
    counts = [entry['count'] for entry in spot_type_counts]

    total_spots = TouristSpot.objects.filter(municipal=municipal).count()

    total_photos = TouristSpot.objects.filter(municipal=municipal).exclude(photo='path/to/default/FB_IMG_1692936618339.jpg').count()
    
    context = {
        "most_common_spot_type": most_common_spot_type['spot_type'] if most_common_spot_type else None,
        "total_spots": total_spots, 
        "spot_type_counts": spot_type_counts,
        "spot_types": spot_types,
        "counts": counts,
        "total_photos": total_photos,
        }
    return render(request, 'tourist_spots/dashboard.html', context)

@login_required
@permission_required('barangayApp.can_view_tourist_staff_views', raise_exception=True)
def tourist_spot(request, page=1):
    user = request.user
    municipal = user.municipal
    if not municipal:
        return HttpResponse("You are not associated with any municipal.")

    tourist_spots = TouristSpot.objects.filter(municipal=municipal).order_by('name')
    Tourist_spotsFilter = Tourist_spotsFilters(request.GET, queryset=tourist_spots)
    tourist_spots = Tourist_spotsFilter.qs
    
    filtering = Tourist()

    barangays = Barangay.objects.filter(municipal=municipal)

    p = Paginator(tourist_spots, 10)  
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    start_index = (page.number - 1) * p.per_page

    context = {
        'tourist_spots': page, 
        'start_index': start_index,
        'Tourist_spotsFilter': Tourist_spotsFilters,
        'barangays': barangays, 
        'filtering': filtering
        }
    return render(request, 'tourist_spots/tourist_spots.html', context)

@login_required
@permission_required('barangayApp.can_view_tourist_staff_views', raise_exception=True)
def add_tourist_spot(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        latitude = float(request.POST.get('latitude', 11.5833))
        longitude = float(request.POST.get('longitude', 124.4642))
        spot_type = request.POST.get('spot_type', 'Natural Attraction')
        photo = request.FILES.get('photo')
        

        barangay_id = request.POST.get('barangay', '')
        barangay = get_object_or_404(Barangay, id=barangay_id) if barangay_id else None

        tourist_spot = TouristSpot(
            name=name,
            description=description,
            latitude=latitude,
            longitude=longitude,
            spot_type=spot_type,
            photo=photo,
            barangay=barangay,
        )

        if request.user.user_type == 'tourist_staff':
            tourist_spot.municipal = request.user.municipal
        else:
            municipal = None
        

        tourist_spot.save()
        return redirect('tourist-staff-tourist-spots')  # Assuming there's a URL named 'list_tourist_spots'
    
    context = {
        'SPOT_TYPE_CHOICES': SPOT_TYPE_CHOICES,
    }
    return render(request, 'tourist_spots/add_tourist_spot.html', context)

@login_required
@permission_required('barangayApp.can_view_tourist_staff_views', raise_exception=True)
def edit_tourist_spot(request, pk):
    tourist_spot = get_object_or_404(TouristSpot, id=pk)
    address = tourist_spot.address

    if request.method == "POST":
        tourist_spot.name = request.POST.get("name", tourist_spot.name)
        tourist_spot.description = request.POST.get("description", tourist_spot.description)
        
        # Check if a new photo is provided
        if request.FILES.get('photo'):
            tourist_spot.photo = request.FILES.get("photo")

        tourist_spot.latitude = request.POST.get("latitude", tourist_spot.latitude)
        tourist_spot.longitude = request.POST.get("longitude", tourist_spot.longitude)
        tourist_spot.spot_type = request.POST.get("spot_type", tourist_spot.spot_type)
        
        # barangay_id = request.POST.get("barangay")

        # if barangay_id is not None:
        #     barangay = get_object_or_404(Barangay, id=barangay_id)
        #     tourist_spot.barangay = barangay
        # else:
        #     tourist_spot.barangay = None

        tourist_spot.save()



        return HttpResponseRedirect("/tourist-staff/tourist-spot")

    context = {
        "tourist_spot": tourist_spot,
        "address": address
    }

    return render(request, 'tourist_spots/edit_tourist_spot.html', context)

@login_required
@permission_required('barangayApp.can_view_tourist_staff_views', raise_exception=True)
def delete_tourist_spot(request, pk):
    tourist_spots = TouristSpot.objects.get(id=pk)
    tourist_spots.delete()
    return redirect('tourist-staff-tourist-spots')

@login_required
@permission_required('barangayApp.can_view_tourist_staff_views', raise_exception=True)
def user_settings(request):
    
    return render(request, 'tourist_spots/user_settings.html')

@login_required
@permission_required('barangayApp.can_view_tourist_staff_views', raise_exception=True)
def logout(request):
    return HttpResponse('Logout')