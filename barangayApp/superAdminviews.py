
from .models import *
from .forms import *
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


def my_view(request):
    all_audit_logs = AuditLogEntry.objects.all()
    
def audit_log_view(request):
    audit_logs = LogEntry.objects.all()
    paginator = Paginator(audit_logs, 10)  # Show 10 audit logs per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'super_admin/audit_log.html', {'page_obj': page_obj})

@login_required
@permission_required('barangayApp.can_view_super_admin_views', raise_exception=True)
def dashboard(request):
    municipal_household = Municipal.objects.all()
    municipal_household_counts = [Household.objects.filter(municipal=municipal).count() for municipal in municipal_household]
    municipal_names = [municipal.name for municipal in municipal_household]

    municipals = Municipal.objects.annotate(total_residents=Count('resident'))
    municipal_residents = [municipal.total_residents for municipal in municipals]
    municipal_labels = [municipal.name for municipal in municipals]

    total_residents = Resident.objects.count()
    total_municipals = Municipal.objects.count()
    total_barangays = Barangay.objects.count()
    total_households = Household.objects.count()
    total_users = CustomUser.objects.count()

    most_populated_municipal = Municipal.objects.annotate(residents_count=Count('resident')).order_by('-residents_count').first()
    
    average_ages = Resident.objects.values('municipal__name').annotate(average_age=Round(Avg('age'), 2))
    municipal_average_ages = [item['average_age'] for item in average_ages]
    municipal_names = [item['municipal__name'] for item in average_ages]
    average_age_all = Resident.objects.aggregate(average_age=Round(Avg('age'), 2))['average_age']

    most_common_sex = Resident.objects.values('sex').annotate(sex_count=Count('sex')).order_by('-sex_count').first()

    if most_common_sex:
        most_common_sex = most_common_sex['sex']
    else:
        most_common_sex = None


    sex_ratios = []

    for municipal in municipals:
        females = Resident.objects.filter(municipal=municipal, sex='Female').count()
        males = Resident.objects.filter(municipal=municipal, sex='Male').count()
        
        total_count = females + males

        if total_count != 0:
            female_ratio = (females / total_count) * 100
            male_ratio = (males / total_count) * 100
        else:
            female_ratio = 0
            male_ratio = 0

        sex_ratios.append({
            'municipal': municipal.name,
            'female_count': females,
            'male_count': males,
            'total_count': total_count,
            'female_ratio': female_ratio,
            'male_ratio': male_ratio,
        })


    senior_citizens = Resident.objects.filter(age__gte=60).values('municipal__name').annotate(senior_count=Count('id')).order_by('municipal__name')
    municipal_senior_labels = [item['municipal__name'] for item in senior_citizens]
    municipal_senior_counts = [item['senior_count'] for item in senior_citizens]
    most_senior_municipal = senior_citizens.order_by('-senior_count').first()

    disabilities_data = Health.objects.values('disability').annotate(count=Count('disability')).order_by('-count')[:5]
    disabilities_labels = [item['disability'] for item in disabilities_data]
    disabilities_counts = [item['count'] for item in disabilities_data]

    common_illnesses_data = Health.objects.values('illness', 'resident__municipal__name').annotate(count=Count('illness')).order_by('-count')[:5]
    illnesses_labels = [item['illness'] for item in common_illnesses_data]
    illnesses_counts = [item['count'] for item in common_illnesses_data]
    municipalities = [item['resident__municipal__name'] for item in common_illnesses_data]
    
    context = {
        'municipalities': municipalities,
        'municipal_residents': municipal_residents,
        'municipal_labels': municipal_labels,
        'most_populated_municipal': most_populated_municipal,

        'municipal_household_counts': municipal_household_counts,
        'municipal_names': municipal_names,

        'total_residents': total_residents,
        'total_municipals': total_municipals,
        'total_barangays': total_barangays,
        'total_users': total_users,

        'municipal_average_ages': municipal_average_ages,  # Add this line
        'municipal_names': municipal_names,  # Add this line
        'average_age_all': average_age_all,

        'sex_ratios': sex_ratios,
        'most_common_sex': most_common_sex,

        'municipal_senior_labels': municipal_senior_labels,
        'municipal_senior_counts': municipal_senior_counts,
        'most_senior_municipal': most_senior_municipal,

        'illnesses_labels': illnesses_labels,
        'illnesses_counts': illnesses_counts,

        'disabilities_labels': disabilities_labels,
        'disabilities_counts': disabilities_counts,
        'total_households': total_households
    }
    return render(request, 'super_admin/dashboard.html', context)



@login_required
@permission_required('barangayApp.can_view_super_admin_views', raise_exception=True)   
def household(request, page=1):
    barangays = Barangay.objects.all()
    municipals = Municipal.objects.all()
    households = Household.objects.all()
    household_filter = HouseholdFilters(request.GET, queryset=households)
    households = household_filter.qs

    household_data = []

    for household in households:
        first_name = household.household_head.first_name if household.household_head else 'No Head Assigned'
        # middle_initial = household.household_head.middle_name[0] if household.household_head.middle_name else ''
        # last_name = household.household_head.last_name if household.household_head else ''
        # suffix = household.household_head.suffix if household.household_head else ''

        # full_name = f"{last_name}, {first_name} {middle_initial}. {suffix}"

        household_data.append({
            'latitude': household.latitude,
            'longitude': household.longitude,
            'id': household.id,
            'head_name': first_name
        })

    household_data_json = json.dumps(household_data)

    p = Paginator(households, 10)  
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    start_index = (page.number - 1) * p.per_page

    
    barangays = list(Barangay.objects.all().values('id', 'municipal_id', 'name'))
    barangays_json = json.dumps(barangays)

    context = {
        'households': page,
        'household_filter': household_filter,
        'start_index': start_index,
        'barangays_json': barangays_json,
        'household_data_json': household_data_json,
        'barangays': barangays,
        'municipals': municipals,
        'municipal_ids': [municipal.id for municipal in municipals]
    }

    return render(request, 'super_admin/household.html', context)

@login_required
@permission_required('barangayApp.can_view_super_admin_views', raise_exception=True)   
def resident(request, page=1):
    selected = request.GET.get('selected')
    residents = Resident.objects.all().order_by('last_name')
    resident_filter = ResidentFilters(request.GET, queryset=residents)
    residents = resident_filter.qs
    p = Paginator(residents, 10)  # Set per_page to 10
    page_obj = p.get_page(page)

    page_num = request.GET.get('page', 1)
    page = p.page(page_num)

    # Calculate the starting index of the current page
    start_index = (page.number - 1) * p.per_page
    # Get the list of barangays and convert it to JSON
    barangays = list(Barangay.objects.all().values('id', 'municipal_id', 'name'))
    barangays_json = json.dumps(barangays)

    context = {
        'residents': page,
        'selected': selected,
        'resident_filter': resident_filter,
        'barangays_json': barangays_json,  # Pass the barangays JSON to the template
        'start_index': start_index,
    }

    return render(request, 'super_admin/resident.html', context)



 
@login_required
@permission_required('barangayApp.can_view_super_admin_views', raise_exception=True)      
def settings(request):
    return HttpResponse('Settings')

def logout(request):
    return HttpResponse('Logout')

def view_resident(request, pk):
    resident = Resident.objects.get(id = pk)
    if resident != None:
        return render(request, 'barangayAdmin/edit_resident.html', {'editResidents':editResidents})


def add_municipal(request):
    if request.method=="POST":
        if request.POST.get('name') \
            and request.POST.get('zip_code') :
            municipal = Municipal()
            municipal.name = request.POST.get('name')
            municipal.zip_code = request.POST.get('zip_code')
            municipal.save()
            messages.success(request, 'Municipal added successfully')
            return HttpResponseRedirect(reverse('super-admin-municipal'))

    else:
            return render(request, 'super_admin/add_municipal.html')

@login_required
@permission_required('barangayApp.can_view_super_admin_views', raise_exception=True)    
def edit_municipal(request, pk):
    municipal = get_object_or_404(Municipal, id=pk)
    if request.method == "POST":
        municipal.name = request.POST.get('name')
        municipal.zip_code = request.POST.get('zip_code')
        municipal.save()
        messages.success(request, 'Municipal updated successfully')
        return HttpResponseRedirect('/super-admin/municipal')
    else:
        return render(request, 'super_admin/edit_municipal.html')

def add_barangay(request):
    if request.method == "POST":
        form = BarangayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Barangay added successfully')
        return HttpResponseRedirect('/super-admin/barangay')
    else:
        form = BarangayForm()

    context = {
        'form': form,
    }
    return render(request, 'super_admin/add_barangay.html', context)

def edit_barangay(request, pk):
    barangay = get_object_or_404(Barangay, pk=pk)

    if request.method == 'POST':
        form = BarangayForm(request.POST, instance=barangay)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/super-admin/barangay')
    else:
        form = BarangayForm(instance=barangay)



def edit_user(request, pk):
    user = get_object_or_404(CustomUser, id=pk)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('super-admin-manage-user')
    else:
        form = UserEditForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'super_admin/edit_user.html', context)


def delete_municipal(request, pk):
    municipal = Municipal.objects.get(id=pk)
    municipal.delete()
    return redirect("super-admin-municipal")

def delete_barangay(request, pk):
    barangay = Barangay.objects.get(id=pk)
    barangay.delete()
    return redirect("super-admin-barangay")

def register(request):
    if request.method == 'POST':
        form = SuperUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            return redirect('super-admin-manage-user')  
    else:
        form = SuperUserRegistrationForm() 
    
    context = {'form': form}
    return render(request, 'super_admin/register_user.html', context)


@login_required
@permission_required('barangayApp.can_view_super_admin_views', raise_exception=True)   
def manage_users(request, page=1):
    selected = request.GET.get('selected')

    users = CustomUser.objects.all()
    
    p = Paginator(users, 10)
    page_obj = p.get_page(page)
    
    start_index = (page_obj.number - 1) * p.per_page

    form_instances = []
    for user in page_obj:
        form = SuperUserRegistrationForm(instance=user)
        form_instances.append(form)

    context = {
        'users': zip(page_obj, form_instances),
        'selected': selected,
        'page_obj': page_obj,
        'form': SuperUserRegistrationForm(),
        'start_index': start_index,
    }
    
    return render(request, 'super_admin/manage_users.html', context)

class ExportResidentsPDFView(View):
    def get(self, request):
        residents = Resident.objects.all()
        resident_filter = ResidentFilters(request.GET, queryset=residents)
        filtered_residents = resident_filter.qs

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resident_report.pdf"'

        pdf = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        table_data = [['Name', 'Age', 'Vaccination', 'Status', 'Birthdate']]  # Header row

        for resident in filtered_residents:
            row = [f"{resident.last_name}, {resident.first_name} {resident.middle_name} {resident.suffix}", 
                    resident.age, 
                    resident.vaccination, 
                    resident.status, 
                    resident.birth_date]

            table_data.append(row)

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centered alignment for all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font style
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header row font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row bottom padding
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),  # Data rows background color
        ]))

        elements.append(table)

        pdf.build(elements)

        return response


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password successfully changed.')
            return redirect('profile')  
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request, 'super_admin/change_password.html', {'form': form})

@login_required
@permission_required('barangayApp.can_view_super_admin_views', raise_exception=True)   
def user_settings(request):
    return render(request, 'super_admin/user_settings.html')