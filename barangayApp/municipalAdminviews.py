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
@permission_required('barangayApp.can_view_municipal_admin_views', raise_exception=True)
def dashboard(request):
    user = request.user
    municipal = user.municipal
    
    if not municipal:
        return HttpResponse("You are not associated with any municipal.")
    
    total_residents = Resident.objects.filter(municipal=municipal).count()
    total_households = Household.objects.filter(municipal=municipal).count()
    total_members = Household.objects.filter(municipal=municipal).aggregate(total_members=Count('members'))['total_members']
    average_members = Household.objects.filter(municipal=municipal).aggregate(average_members=Round(Avg('num_members'), 2))['average_members']
    
    household_data = Household.objects.filter(municipal=municipal).aggregate(
        num_senior_citizens=Count('num_senior_citizens', distinct=True),
        num_pregnant_lactating_mothers=Count('num_pregnant_lactating_mothers', distinct=True),
        num_beneficiaries_with_disability=Count('num_beneficiaries_with_disability', distinct=True),
        num_registered_voters=Count('num_registered_voters', distinct=True),
        num_members=Count('members', distinct=True)
    )

    total_senior_citizens = Household.objects.filter(municipal=municipal).aggregate(total_senior_citizens=Count('num_senior_citizens'))['total_senior_citizens']
    total_pregnant_lactating_mothers = Household.objects.filter(municipal=municipal).aggregate(total_pregnant_lactating_mothers=Count('num_pregnant_lactating_mothers'))['total_pregnant_lactating_mothers']
    total_beneficiaries_with_disability = Household.objects.filter(municipal=municipal).aggregate(total_beneficiaries_with_disability=Count('num_beneficiaries_with_disability'))['total_beneficiaries_with_disability']
    total_registered_voters = Household.objects.filter(municipal=municipal).aggregate(total_registered_voters=Count('num_registered_voters'))['total_registered_voters']

    gender_distribution = Resident.objects.filter(municipal=municipal).values('sex').annotate(count=Count('sex'))
    gender_labels = [entry['sex'] for entry in gender_distribution]
    gender_counts = [entry['count'] for entry in gender_distribution]

    age_distribution = Resident.objects.filter(municipal=municipal) \
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

    worker_counts = Economic.objects.filter(resident__municipal=municipal) \
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
    return render(request, 'municipalAdmin/dashboard.html', context)

@login_required
@permission_required('barangayApp.can_view_municipal_admin_views', raise_exception=True)      
def barangay(request):
    barangays = Barangay.objects.all()
    paginator = Paginator(barangays, 10)  # Change the number '10' to the desired number of items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = BarangayForm()
    if request.method == 'POST':
        form = BarangayForm(request.POST)
        if form.is_valid():
            form.save()
            
    context = {
        'barangays': page_obj,
        'form': form
    }
    return render(request, 'municipalAdmin/barangay.html', context)

@login_required
@permission_required('barangayApp.can_view_municipal_admin_views', raise_exception=True)   
def household(request, page=1):
    user = request.user
    municipal = user.municipal
    if not municipal:
        return HttpResponse("You are not associated with any municipal.")

    households = Household.objects.filter(municipal=municipal).order_by('household_head__last_name')
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

    municipal_geojson = municipal.geom.geojson if municipal and municipal.geom else None

    context = {
        'households': page,
        'household_filter': household_filter,
        'start_index': start_index,
        'household_data_json': household_data_json,
        'municipal_geojson': municipal_geojson
    }
    return render(request, 'municipalAdmin/household.html', context)


@login_required
@permission_required('barangayApp.can_view_municipal_admin_views', raise_exception=True)   
def resident(request):
    user = request.user
    municipal = user.municipal
    if not municipal:
        return HttpResponse("You are not associated with any municipal.")

    residents = Resident.objects.filter(municipal=municipal).order_by('last_name')
    households = Household.objects.filter(municipal=municipal)
    
    # Filter Barangay objects based on the municipal associated with the user
    barangays = Barangay.objects.filter(municipal=municipal)

    resident_filter = ResidentFilters(request.GET, queryset=residents)
    householdFilter = HouseholdFilters(request.GET, queryset=households)
    barangayFilter = BarangayFilters(request.GET, queryset=barangays)
    
    residents = resident_filter.qs

    p = Paginator(residents, 10)  
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    start_index = (page.number - 1) * p.per_page

    context = {
        'residents': page, 
        'resident_filter': resident_filter, 
        'householdFilter': householdFilter, 
        'barangayFilter': barangayFilter,  # Add this line
        'start_index': start_index,
    }
    return render(request, 'municipalAdmin/resident.html', context)

@login_required
@permission_required('barangayApp.can_view_municipal_admin_views', raise_exception=True)   
def logout(request):
    logout(request)
    return HttpResponse('Logout')

@login_required
@permission_required('barangayApp.can_view_municipal_admin_views', raise_exception=True)   
def manage_users(request, page=1):
    selected = request.GET.get('selected')
    
    # Get the municipal of the logged-in user
    user = request.user
    municipal = user.municipal

    # Check if the user is associated with any municipal
    if not municipal:
        return HttpResponse("You are not associated with any municipal.")

    # Specify the user types you want to filter
    user_types_to_filter = ['tourist_staff', 'barangay_staff', 'barangay_admin']
    
    # Use Q objects to construct the OR condition for user types
    user_type_condition = Q()
    for user_type in user_types_to_filter:
        user_type_condition |= Q(user_type=user_type)
    
    # Filter users based on the specified user types and municipal
    users = CustomUser.objects.filter(user_type_condition, barangay__municipal=municipal)
    
    p = Paginator(users, 10)
    page_obj = p.get_page(page)

    form_instances = []
    
    for user in page_obj:
        form = MunicipalUserRegistrationForm(instance=user, user=request.user)
        form_instances.append(form)

    context = {
        'users': zip(page_obj, form_instances),
        'selected': selected,
        'user_types': user_types_to_filter,
        'page_obj': page_obj,
        'form': MunicipalUserRegistrationForm()  # Use the same form class for registration and editing
    }
    
    return render(request, 'municipalAdmin/manage_users.html', context)


@login_required
@permission_required('barangayApp.can_view_municipal_admin_views', raise_exception=True)   
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('municipal-admin-manage-user')
    else:
        form = UserEditForm(instance=user)

    context = {
            'form': form, 
            'user': user
            }
    return render(request, 'municipalAdmin/edit_user.html', context)

@login_required
@permission_required('barangayApp.can_view_municipal_admin_views', raise_exception=True)  
def register(request):
    if request.method == 'POST':
        form = MunicipalUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            return redirect('municipal-admin-manage-user')  
    else:
        form = MunicipalUserRegistrationForm() 
    
    context = {'form': form}
    return render(request, 'municipalAdmin/register_user.html', context)