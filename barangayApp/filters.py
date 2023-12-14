from .models import *
from django import forms
from django_filters.widgets import RangeWidget
from django.db.models import Q, CharField, Value

import django_filters

class ResidentFilters(django_filters.FilterSet):
    STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Annuled', 'Annuled'),
        ('Widowed', 'Widowed'),
        ('Separated', 'Separated'),
        ('Common Law/Live in', 'Common Law/Live in'),
        ('Unknown', 'Unknown'),
    ]
    VACCINATION_CHOICES = [
        ('Vaccinated', 'Vaccinated'),
        ('Not Vaccinated', 'Not Vaccinated'),
    ]
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    PREGNANCY_STATUS = (
        ('Pregnant', 'Pregnant'),
        ('Not Pregnant', 'Not Pregnant'),
        ('Prefer not to say', 'Prefer not to say'),
    )
    MALNURISHED_STATUS = (
        ('Severe malnutrition', 'Severe malnutrition'),
        ('Moderate malnutrition', 'Moderate malnutrition'),
        ('Mild malnutrition', 'Mild malnutrition'),
        ('No malnutrition', 'No malnutrition'),
    )

    municipal = django_filters.ModelChoiceFilter(
        field_name='barangay__municipal',
        queryset=Municipal.objects.all(),
        label='Municipal',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
    barangay = django_filters.ModelChoiceFilter(
        field_name='barangay',
        queryset=Barangay.objects.all(),
        label='Barangay',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
   
    name = django_filters.CharFilter(
        method='filter_search_name',
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    age = django_filters.NumberFilter(
        field_name='age',
        lookup_expr='exact',
        label='Age',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'})
    )
    age__lt = django_filters.NumberFilter(
        field_name='age',
        lookup_expr='lt',
        label='Age (less than)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'})
    )
    age__gt = django_filters.NumberFilter(
        field_name='age',
        lookup_expr='gt',
        label='Age (greater than)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'})
    )
    age__range = django_filters.RangeFilter(
        field_name='age',
        label='Age Range',
        widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control'})
    )

    vaccination = django_filters.MultipleChoiceFilter(
        field_name='vaccination',
        choices=VACCINATION_CHOICES,
        label='Vaccination',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
    sex = django_filters.MultipleChoiceFilter(
        field_name='sex',
        choices=SEX_CHOICES,
        label='Sex',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
    status = django_filters.MultipleChoiceFilter(
        field_name='status',
        choices=STATUS_CHOICES,
        label='Status',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
    
   
    highest_education = django_filters.MultipleChoiceFilter(
        method='filter_education_level',
        choices=(
            EDUCATIONLEVEL0 + EDUCATIONLEVEL1 +
            EDUCATIONLEVEL2 + EDUCATIONLEVEL3 + EDUCATIONLEVEL4
        ),
        label='Highest Education Attainment',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    master_doctoral_education = django_filters.MultipleChoiceFilter(
        field_name='education__master_doctoral_education',
        choices=EDUCATIONLEVEL5,
        label='Master/Doctoral Education',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
    curriculum_strands = django_filters.MultipleChoiceFilter(
        field_name='education__curriculum_strands',
        choices=STRAND,
        label='Curriculum Strands',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
    undergraduate_reason = django_filters.MultipleChoiceFilter(
        field_name='education__undergraduate_reason',
        choices=REASON,
        label='Undergraduate Reason',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    specific_occupation = django_filters.CharFilter(
        field_name='economic__specific_occupation',
        label='Specific Occupation',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    industry_of_work = django_filters.CharFilter(
        field_name='economic__industry_of_work',
        label='Industry of Work',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    working_arrangement = django_filters.MultipleChoiceFilter(
        field_name='economic__working_arrangement',
        choices=ARRANGEMENT,
        label='Working Arrangement',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    nature_of_employment = django_filters.MultipleChoiceFilter(
        field_name='economic__nature_of_employment',
        choices=EMPLOYMENT,
        label='Nature of Employment',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})

    )

    class_of_worker = django_filters.MultipleChoiceFilter(
        field_name='economic__class_of_worker',
        choices=WORKER,
        label='Class of Worker',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    basis_of_payment = django_filters.MultipleChoiceFilter(
        field_name='economic__basis_of_payment',
        choices=PAYMENT,
        label='Basis of Payment',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    disability = django_filters.MultipleChoiceFilter(
        field_name='health__disability',
        choices=DISABILITY,
        label='Disability',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    illness = django_filters.MultipleChoiceFilter(
        field_name='health__illness',
        choices=ILLNESS,
        label='Illness',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    pregnancy_status = django_filters.MultipleChoiceFilter(
        field_name='health__pregnancy_status',
        choices=PREGNANCY_STATUS,
        label='Pregnancy Status',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    malnutrition_status = django_filters.MultipleChoiceFilter(
        field_name='health__malnutrition_status',
        choices=MALNURISHED_STATUS,
        label='Malnutrition Status',
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    class Meta:
        model = Resident
        fields = [
            'municipal',
            'barangay',
            'name',
            'sex',
            'age',
            'age__lt',
            'age__gt',
            'age__range',
            'vaccination',
            'status',
            # 'early_childhood_education',
            # 'primary_education',
            # 'lower_secondary_education',
            # 'upper_secondary_education',
            # 'bachelor_education',

            'highest_education',

            'master_doctoral_education',
            'curriculum_strands',
            'undergraduate_reason',
            'specific_occupation',
            'industry_of_work',
            'working_arrangement',
            'nature_of_employment',
            'class_of_worker',
            'basis_of_payment',
            'disability',
            'illness',
            'pregnancy_status',
            'malnutrition_status',
        ]

    def filter_search_name(self, queryset, name, value):
        if value:
            words = value.split()
            for word in words:
                queryset = queryset.filter(
                    Q(suffix__icontains=word) |
                    Q(first_name__icontains=word) |
                    Q(middle_name__icontains=word) |
                    Q(last_name__icontains=word)
                )
            return queryset
        return queryset

    def filter_education_level(self, queryset, name, value):
        if value:
            # Iterate over each education level choice
            for level in value:
                # Form a Q object to check if any of the education fields contains the chosen level
                q = Q()
                for field in ['early_childhood_education', 'primary_education', 'lower_secondary_education', 'upper_secondary_education', 'bachelor_education']:
                    q |= Q(**{f'education__{field}__icontains': level})
                
                # Apply the Q object to the queryset
                queryset = queryset.filter(q)
                
            return queryset
        return queryset

class HouseholdFilters(django_filters.FilterSet): 
    barangay = django_filters.ModelChoiceFilter(
        field_name='barangay',
        queryset=Barangay.objects.all(),
        label='Barangay',
        empty_label='All',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    municipal = django_filters.ModelChoiceFilter(
        field_name='municipal',
        queryset=Municipal.objects.all(),
        label='Municipal',
        empty_label='All',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    household_head__full_name = django_filters.CharFilter(
        method='filter_head_full_name',
        label='Household Head Name Contains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    members__full_name = django_filters.CharFilter(
        method='filter_members_full_name',
        label='Members Name Contains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    num_senior_citizens = django_filters.NumberFilter(
        field_name='num_senior_citizens',
        lookup_expr='exact',
        label='Number of Senior Citizens',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    num_pregnant_lactating_mothers = django_filters.NumberFilter(
        field_name='num_pregnant_lactating_mothers',
        lookup_expr='exact',
        label='Number of Pregnant/Lactating Mothers',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    num_beneficiaries_with_disability = django_filters.NumberFilter(
        field_name='num_beneficiaries_with_disability',
        lookup_expr='exact',
        label='Number of Beneficiaries with Disability',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    
    name_contains = django_filters.CharFilter(
        method='filter_name_contains',
        label='Name Contains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    num_registered_voters = django_filters.NumberFilter(
        field_name='num_registered_voters',
        lookup_expr='exact',
        label='Number of Registered Voters',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    monthly_income_range = django_filters.MultipleChoiceFilter(
        choices=INCOME_RANGE,
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
    
    education_level_of_head = django_filters.MultipleChoiceFilter(
        choices=EDUCATION_LEVEL_HEAD,
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    access_to_basic_amenities = django_filters.MultipleChoiceFilter(
        choices=ACCESS_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    ownership_of_assets = django_filters.MultipleChoiceFilter(
        choices=OWNERSHIP_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )
    
    housing_condition = django_filters.MultipleChoiceFilter(
        choices=HOUSE_CONDITION,
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    household_type = django_filters.MultipleChoiceFilter(
        choices=HOUSEHOLD_TYPE_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'selectpicker', 'data-live-search': 'true'})
    )

    def filter_head_full_name(self, queryset, name, value):
        return queryset.filter(
            Q(household_head__first_name__icontains=value) |
            Q(household_head__middle_name__icontains=value) |
            Q(household_head__last_name__icontains=value) |
            Q(household_head__suffix__icontains=value)
        )

    def filter_members_full_name(self, queryset, name, value):
        return queryset.filter(
            Q(members__first_name__icontains=value) |
            Q(members__middle_name__icontains=value) |
            Q(members__last_name__icontains=value) |
            Q(members__suffix__icontains=value)
        )

    class Meta:
        model = Household
        fields = [
            'household_head__full_name', 
            'members__full_name', 
            'barangay', 
            'municipal', 
            'housing_condition',
            'household_type',
            'monthly_income_range',
            'num_senior_citizens',
            'num_pregnant_lactating_mothers',
            'num_registered_voters',
            'education_level_of_head',
            'access_to_basic_amenities',
            'ownership_of_assets',
            ]

class Tourist_spotsFilters(django_filters.FilterSet):

    name = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter spot name...'})
    )

    spot_type = django_filters.ChoiceFilter(
        choices=SPOT_TYPE_CHOICES,
        label='Tourist Spot Type',
        empty_label='All',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    barangay = django_filters.ModelChoiceFilter(
        field_name='barangay',
        queryset=Barangay.objects.all(),
        label='Barangay',
        empty_label='All',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    municipal = django_filters.ModelChoiceFilter(
        field_name='municipal',
        queryset=Municipal.objects.all(),
        label='Municipal',
        empty_label='All',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = TouristSpot
        fields = [
            'name',
            'spot_type',
            'barangay',
            'municipal'
        ]

# class Tourist_spotsFilters(django_filters.FilterSet):
#     spot_type = django_filters.ChoiceFilter(
#         field_name='spot_type',
#         choices=TouristSpot.SPOT_TYPE_CHOICES,
#         label='Spot Type',
#     )

#     class Meta:
#         model = TouristSpot
#         fields = ['spot_type']

class Tourist(django_filters.FilterSet): 
    class Meta:
        model = TouristSpot
        fields = [
            'name',
            'spot_type',
        ]

class BarangayFilters(django_filters.FilterSet): 
    barangay = django_filters.ModelChoiceFilter(
        field_name='barangay',
        queryset=Barangay.objects.all(),
        label='Barangay',
        empty_label='All',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    municipal = django_filters.ModelChoiceFilter(
        field_name='municipal',
        queryset=Municipal.objects.all(),
        label='Municipal',
        empty_label='All',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Barangay
        fields = [
            'barangay',
            'municipal',
            'name_2',
            'id_3',
            'name',
        ]


