from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseServerError, HttpResponse, FileResponse
from .models import *
from .forms import *
from .filters import *
from django.db.models import Q, Sum, Count, Avg, Case, When, Value, F
from django.db.models.functions import Round
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission

import json

@login_required
@permission_required('barangayApp.can_view_barangay_admin_views', raise_exception=True)
def dashboard(request):
    user = request.user
    barangay = user.barangay
    
    if not barangay:
        return HttpResponse("You are not associated with any barangay.")
    
    total_residents = Resident.objects.filter(barangay=barangay).count()
    total_households = Household.objects.filter(barangay=barangay).count()
    total_members = Household.objects.filter(barangay=barangay).aggregate(total_members=Count('members'))['total_members']
    average_members = Household.objects.filter(barangay=barangay).aggregate(average_members=Round(Avg('num_members'), 2))['average_members']

    household_data = Household.objects.filter(barangay=barangay).aggregate(
        num_senior_citizens=Count('num_senior_citizens', distinct=True),
        num_pregnant_lactating_mothers=Count('num_pregnant_lactating_mothers', distinct=True),
        num_beneficiaries_with_disability=Count('num_beneficiaries_with_disability', distinct=True),
        num_registered_voters=Count('num_registered_voters', distinct=True),
        num_members=Count('members', distinct=True)
    )

    total_senior_citizens = Household.objects.filter(barangay=barangay).aggregate(total_senior_citizens=Count('num_senior_citizens'))['total_senior_citizens']
    total_pregnant_lactating_mothers = Household.objects.filter(barangay=barangay).aggregate(total_pregnant_lactating_mothers=Count('num_pregnant_lactating_mothers'))['total_pregnant_lactating_mothers']
    total_beneficiaries_with_disability = Household.objects.filter(barangay=barangay).aggregate(total_beneficiaries_with_disability=Count('num_beneficiaries_with_disability'))['total_beneficiaries_with_disability']
    total_registered_voters = Household.objects.filter(barangay=barangay).aggregate(total_registered_voters=Count('num_registered_voters'))['total_registered_voters']

    gender_distribution = Resident.objects.filter(barangay=barangay).values('sex').annotate(count=Count('sex'))
    gender_labels = [entry['sex'] for entry in gender_distribution]
    gender_counts = [entry['count'] for entry in gender_distribution]

    age_distribution = Resident.objects.filter(barangay=barangay) \
        .annotate(age_group=Case(
            When(age__lt=18, then=Value('0-17')),
            When(age__range=[18, 25], then=Value('18-25')),
            When(age__range=[26, 35], then=Value('26-35')),
            When(age__range=[36, 50], then=Value('36-50')),
            When(age__range=[51, 60], then=Value('51-60')),
            When(age__gte=61, then=Value('60+')),
            default=Value('Unknown'),
            output_field=models.CharField(),
        )) \
        .values('age_group') \
        .annotate(count=Count('id'))

    age_labels = [item['age_group'] for item in age_distribution]
    age_counts = [item['count'] for item in age_distribution]

    worker_counts = Economic.objects.filter(resident__barangay=barangay) \
        .values('class_of_worker') \
        .annotate(count=Count('class_of_worker')) \
        .order_by('-count')[:2] 

    chart_data = {
        'labels': [item['class_of_worker'] for item in worker_counts],
        'data': [item['count'] for item in worker_counts],
    }

    chart_data_json = json.dumps(chart_data)


    context = {
        "total_residents": total_residents, 
        "total_households": total_households, 
        "total_members": total_members,
        "total_senior_citizens": total_senior_citizens,
        "total_pregnant_lactating_mothers": total_pregnant_lactating_mothers,
        "total_beneficiaries_with_disability": total_beneficiaries_with_disability,
        "total_registered_voters": total_registered_voters,

        "gender_labels": gender_labels,
        "gender_counts": gender_counts,
        "age_labels": age_labels,
        "age_counts": age_counts,
        "average_members": average_members,
        "chart_data": chart_data_json,
        }
    return render(request, 'barangayAdmin/dashboard.html', context)

@login_required
@permission_required('barangayApp.can_view_barangay_admin_views', raise_exception=True)      
def household(request, page=1):
    user = request.user
    barangay = user.barangay
    if not barangay:
        return HttpResponse("You are not associated with any barangay.")

    households = Household.objects.filter(barangay=barangay).order_by('household_head__last_name')
    household_filter = HouseholdFilters(request.GET, queryset=households)
    households = household_filter.qs

    household_data = []

    for household in households:
        first_name = household.household_head.first_name if household.household_head else 'No Head Assigned'
        middle_initial = household.household_head.middle_name[0] if household.household_head.middle_name else ''
        last_name = household.household_head.last_name if household.household_head else ''
        suffix = household.household_head.suffix if household.household_head else ''

        full_name = f"{last_name}, {first_name} {middle_initial}. {suffix}"

        household_data.append({
            'latitude': household.latitude,
            'longitude': household.longitude,
            'id': household.id,
            'head_name': full_name
        })

    household_data_json = json.dumps(household_data)

    p = Paginator(households, 10)  
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    start_index = (page.number - 1) * p.per_page

    barangay_geojson = barangay.geom.geojson if barangay and barangay.geom else None

    context = {
        'households': page,
        'household_filter': household_filter,
        'start_index': start_index,
        'household_data_json': household_data_json,
        'barangay_geojson': barangay_geojson
    }
    return render(request, 'barangayAdmin/household.html', context)

@login_required
@permission_required('barangayApp.can_view_barangay_admin_views', raise_exception=True)
def resident(request):
    user = request.user
    barangay = user.barangay
    if not barangay:
        return HttpResponse("You are not associated with any barangay.")

    residents = Resident.objects.filter(barangay=barangay).order_by('last_name')
    
    # Apply filters if they exist in the request
    if request.GET:
        resident_filter = ResidentFilters(request.GET, queryset=residents)
        residents = resident_filter.qs
    else:
        resident_filter = ResidentFilters(queryset=residents)

    p = Paginator(residents, 10)  
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    start_index = (page.number - 1) * p.per_page

    context = {
        'residents': page, 
        'resident_filter': resident_filter, 
        'start_index': start_index,
    }
    return render(request, 'barangayAdmin/resident.html', context)

@login_required
@permission_required('barangayApp.can_view_barangay_admin_views', raise_exception=True)
def settings(request):
    return HttpResponse('Settings')

@login_required
@permission_required('barangayApp.can_view_barangay_admin_views', raise_exception=True)
def logout(request):
    return HttpResponse('Logout')

@login_required
@permission_required('barangayApp.can_view_barangay_admin_views', raise_exception=True)
def view_resident(request, pk):
    resident = Resident.objects.get(id = pk)
    if resident != None:
        return render(request, 'barangayAdmin/edit_resident.html', {'editResidents':editResidents})

@login_required
@permission_required('barangayApp.can_view_barangay_admin_views', raise_exception=True)   
def user_settings(request):
    return render(request, 'barangayAdmin/user_settings.html')

