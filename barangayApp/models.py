from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.hashers import make_password

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils import timezone

from datetime import datetime, date

from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

class Municipal(models.Model):
    id_2 = models.BigIntegerField(null=True)
    name = models.CharField(max_length=100, null=True)
    geom = models.MultiPolygonField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    history = AuditlogHistoryField()
    
class Barangay(models.Model):
    municipal = models.ForeignKey(Municipal, on_delete=models.CASCADE, null=True)
    name_2 = models.CharField(max_length=100, null=True)
    id_3 = models.CharField(max_length=11, null=True)
    name = models.CharField(max_length=100, null=True)
    geom = models.MultiPolygonField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    history = AuditlogHistoryField()

class Address(models.Model):
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=255, blank=True, null=True)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True, blank=True)
    municipal = models.ForeignKey(Municipal, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.building}, {self.barangay}, {self.municipal}, Biliran"

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('super_admin', 'Super Admin'),
        ('provincial_admin', 'Provincial Admin'),
        ('municipal_admin', 'Municipal Admin'),
        ('barangay_admin', 'Barangay Admin'),
        ('barangay_staff', 'Barangay Staff'),
        ('tourist_staff', 'Tourist Officer'),
    )

    DEFAULT_PROVINCIAL = 'Biliran'

    user_type = models.CharField(max_length=50, choices=USER_TYPES)
    # is_active = models.BooleanField(default=True)
    provincial = models.CharField(max_length=50, default=DEFAULT_PROVINCIAL)
    municipal = models.ForeignKey(Municipal, on_delete=models.SET_NULL, null=True, blank=True)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['username']
        
        permissions = [
            ('can_view_super_admin_views', 'Can view super admin views'),
            ('can_view_provincial_admin_views', 'Can view provincial admin views'),
            ('can_view_municipal_admin_views', 'Can view municipal admin views'),
            ('can_view_municipal_staff_views', 'Can view municipal staff views'),
            ('can_view_barangay_admin_views', 'Can view barangay admin views'),
            ('can_view_barangay_staff_views', 'Can view barangay staff views'),
            ('can_view_tourist_staff_views', 'Can view tourist staff views'),
        ]

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

        # Assign permissions based on user type
        if self.user_type == 'super_admin':
            self.user_permissions.set([
                Permission.objects.get(codename='can_view_super_admin_views')
            ])
        elif self.user_type == 'provincial_admin':
            self.user_permissions.set([
                Permission.objects.get(codename='can_view_provincial_admin_views')
            ])
        elif self.user_type == 'municipal_admin':
            self.user_permissions.set([
                Permission.objects.get(codename='can_view_municipal_admin_views')
            ])
        elif self.user_type == 'municipal_staff':
            self.user_permissions.set([
                Permission.objects.get(codename='can_view_municipal_staff_views')
            ])
        elif self.user_type == 'barangay_admin':
            self.user_permissions.set([
                Permission.objects.get(codename='can_view_barangay_admin_views')
            ])
        elif self.user_type == 'barangay_staff':
            self.user_permissions.set([
                Permission.objects.get(codename='can_view_barangay_staff_views')
            ])
        elif self.user_type == 'tourist_staff':
            self.user_permissions.set([
                Permission.objects.get(codename='can_view_tourist_staff_views')
            ])

    def __str__(self):
        return self.username
    
    history = AuditlogHistoryField()

SEX = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

STATUS = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Annuled', 'Annuled'),
    ('Widowed', 'Widowed'),
    ('Separated', 'Separated'),
    ('Common Law/Live-in', 'Common Law/Live-in'),
    ('Unknown', 'Unknown'),
)

VACCINATION = (
    ('Vaccinated', 'Vaccinated'),
    ('Not Vaccinated', 'Not Vaccinated'),
)


SCALE = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('I do`t know', 'I don`t know'),
)

ISSUE = (
    ('Seeing', 'Seeing'),
    ('Hearing', 'Hearing'),
    ('Walking', 'Walking'),
    ('Memory', 'Memory'),
    ('Self-caring', 'Self-caring'),
    ('Communicating', 'Communicating'),

)

class Resident(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)      
    last_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)  
    suffix = models.CharField(max_length=50, null=True, blank=True) 
    age = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=50, null=True, blank=True, choices=SEX)
    vaccination = models.CharField(max_length=50, null=True, blank=True, choices=VACCINATION)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS)
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, null=True)
    municipal = models.ForeignKey(Municipal, on_delete=models.CASCADE, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        ordering = ['last_name']
    
    def __str__(self):
        full_name = f"{self.last_name}, {self.first_name}"
        if self.middle_name:
            full_name += f" {self.middle_name}"
        if self.suffix:
            full_name += f" {self.suffix}"
        return full_name
    
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name, self.suffix]
        return ' '.join(filter(None, parts))

    def __str__(self):
        return self.full_name()
        
    history = AuditlogHistoryField()


HOUSE_CONDITION = (
    ('Owned', 'Owned'),
    ('Rented', 'Rented'),
    ('Government Housing', 'Government Housing'),
    ('Informal Settlement', 'Informal Settlement'),
    ('Other', 'Other'),
)

INCOME_RANGE = (
    ('Less than ₱10,000', 'Less than ₱10,000'),
    ('₱10,000 - ₱20,000', '₱10,000 - ₱20,000'),
    ('₱20,000 - ₱30,000', '₱20,000 - ₱30,000'),
    ('₱30,000 - ₱40,000', '₱30,000 - ₱40,000'),
    ('More than ₱40,000', 'More than ₱40,000'),
)

EDUCATION_LEVEL_HEAD = (
    ('No Formal Education', 'No Formal Education'),
    ('Elementary School', 'Elementary School'),
    ('High School Graduate', 'High School Graduate'),
    ('College Graduate', 'College Graduate'),
    ('Postgraduate Degree', 'Postgraduate Degree')
)

ACCESS_CHOICES = (
    ('Electricity', 'Electricity'),
    ('Clean Water', 'Clean Water'),
    ('Sanitation', 'Sanitation'),
    ('Housing', 'Housing'),
    ('Health Services', 'Health Services'),
    ('Education', 'Education'),
    ('Communication', 'Communication'),
    ('Transportation', 'Transportation'),
    ('Others', 'Others'),
)

OWNERSHIP_CHOICES = (
    ('Land', 'Land'),
    ('House', 'House'),
    ('Vehicle', 'Vehicle'),
    ('Livestock', 'Livestock'),
    ('Appliances', 'Appliances'),
    ('Savings', 'Savings'),
    ('Business', 'Business'),
    ('Other Assets', 'Other Assets'),
)

HOUSEHOLD_TYPE_CHOICES = (
    ('Nuclear Family', 'Nuclear Family'),
    ('Extended Family', 'Extended Family'),
    ('Single Parent Family', 'Single Parent Family'),
    ('Child-Headed Family', 'Child-Headed Family'),
    ('Elderly-Headed Family', 'Elderly-Headed Family'),
    ('Other', 'Other'),
)

class Household(models.Model):
    household_head = models.ForeignKey(Resident, null=True, on_delete=models.SET_NULL, related_name='head_of_household')   
    members = models.ManyToManyField(Resident, related_name='households')
    num_senior_citizens = models.IntegerField(null=True)  
    num_pregnant_lactating_mothers = models.IntegerField(null=True) 
    num_beneficiaries_with_disability = models.IntegerField(null=True) 
    num_registered_voters = models.IntegerField(null=True) 
    num_members = models.IntegerField(null=True) 
    latitude = models.FloatField(default=11.5833)  # Set default latitude value
    longitude = models.FloatField(default=124.4642) 
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, null=True)
    municipal = models.ForeignKey(Municipal, on_delete=models.CASCADE, null=True) 

    housing_condition = models.CharField(max_length=50, null=True, blank=True, choices = HOUSE_CONDITION)
    monthly_income_range = models.CharField(max_length=50, null=True, blank=True, choices = INCOME_RANGE)
    access_to_basic_amenities = models.TextField(null=True, blank=True, choices = ACCESS_CHOICES)
    ownership_of_assets = models.TextField(null=True, blank=True, choices = OWNERSHIP_CHOICES)
    education_level_of_head = models.CharField(max_length=50, null=True, blank=True, choices = EDUCATION_LEVEL_HEAD)

    household_type = models.CharField(max_length=50, null=True, blank=True, choices = HOUSEHOLD_TYPE_CHOICES)

    def __str__(self):
        return self.household_head.first_name if self.household_head else 'No Head Assigned'

    history = AuditlogHistoryField()


DISABILITY = (
    ('Visual Disability', 'Visual Disability'),
    ('Hearing Disability', 'Hearing Disability'),
    ('Intellectual Disability', 'Intellectual Disability'),
    ('Learning Disability', 'Learning Disability'),
    ('Mental Disability', 'Mental Disability'),
    ('Physical Disability', 'Physical Disability'),
    ('Psychosocial Disability', 'Psychosocial Disability'),
    ('Speech and Language Impairment', 'Speech and Language Impairment'),
)

ILLNESS = (
    ('Diabetes', 'Diabetes'),
    ('Cancer', 'Cancer'),
    ('Hypertension', 'Hypertension'),
    ('Tuberculosis (TB)', 'Tuberculosis (TB)'),
    ('Acute Respiratory Infection', 'Acute Respiratory Infection'),
    ('Acute Gastroenteritis', 'Acute Gastroenteritis'),
    ('Common Colds, Cough, Flu/Fever', 'Common Colds, Cough, Flu/Fever'),
    ('Cut/Wound', 'Cut/Wound'),
    ('Burn', 'Burn'),
    ('Fracture', 'Fracture'),
    ('Dislocation', 'Dislocation'),
    ('Surgical Illness', 'Surgical Illness'),
    ('Covid-19', 'Covid-19'),
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

class Health(models.Model):
    date_recorded = models.DateField()  # Date of the health record
    disability = models.CharField(max_length=50, null=True, choices=DISABILITY)
    illness = models.CharField(max_length=50, null=True, choices=ILLNESS)
    pregnancy_status = models.CharField(max_length=50, null=True, choices=PREGNANCY_STATUS)
    malnutrition_status = models.CharField(max_length=50, null=True, choices=MALNURISHED_STATUS)

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.resident} - {self.date_recorded}"

    history = AuditlogHistoryField()


EDUCATIONLEVEL0 = (
    ('No Grade Completed', 'No Grade Completed'),
    ('Nursery', 'Nursery'),
    ('Kindergarten', 'Kindergarten'),
)
EDUCATIONLEVEL1 = (
    ('Grade 1', 'Grade 1'),
    ('Grade 2', 'Grade 2 '),
    ('Grade 3', 'Grade 3'),
    ('Grade 4', 'Grade 4'),
    ('Grade 6', 'Grade 5'),
    ('Grade 6', 'Grade 6'),
)
EDUCATIONLEVEL2 = (
    ('Grade 7 / 1st year highschool', 'Grade 7 / 1st year highschool'),
    ('Grade 8 / 2nd year highschool', 'Grade 7 / 2nd year highschool'),
    ('Grade 9 / 3rd year highschool', 'Grade 7 / 3rd year highschool'),
    ('Grade 10 / 4th year highschool', 'Grade 7 / 4th year highschool'),
)
EDUCATIONLEVEL3 = (
    ('Grade 11', 'Grade 11'),
    ('Grade 12', 'Grade 12' ),
    
)
STRAND = (
    ('General Academic Strand', 'General Academic Strand'),
    ('Science Technology Engineering and Mathematics', 'Science Technology Engineering and Mathematics' ),
    ('Humanities and Social Sciences', 'Humanities and Social Sciences' ),
    ('Sports Track', 'Sports Track' ),
    ('Arts and Design', 'Arts and Design' ),
    ('Technology and Livelihood Education and Technical - Vocational Livelihood', 'Technology and Livelihood Education and Technical - Vocational Livelihood' ),
    
)
EDUCATIONLEVEL4 = (
    ('1st Year College', '1st Year College'),
    ('2nd Year College', '2nd Year College'),
    ('3rd Year College ', '3rd Year College '),
    ('4th Year College', '4th Year College'),
)
EDUCATIONLEVEL5 = (
    ('Undergraduate', 'Undergraduate'),
)
REASON = (
    ('Illness', 'Illness'),
    ('Accessibility of School', 'Accessibility of School'),
    ('Disability', 'Disability'),
    ('Pregnancy', 'Pregnancy'),
    ('Marriage', 'Marriage'),
    ('High Cost of Education / Financial Concern', 'High Cost of Education / Financial Concern'),
    ('Employment', 'Employment'),
    ('Finished Schooling', 'Finished Schooling'),
    ('Looking For Work', 'Looking For Work'),
    ('Lack of Personal Interest', 'Lack of Personal Interest'),
    ('Too young to go to School', 'Too young to go to School'),
    ('Bullying', 'Bullying'),
    ('Family Matters', 'Family Matters'),
)
class Education(models.Model):
    early_childhood_education = models.CharField(max_length=50, null=True, choices=EDUCATIONLEVEL0)
    primary_education = models.CharField(max_length=50, null=True, choices=EDUCATIONLEVEL1)
    lower_secondary_education = models.CharField(max_length=50, null=True, choices=EDUCATIONLEVEL2)
    upper_secondary_education = models.CharField(max_length=50, null=True, choices=EDUCATIONLEVEL3)
    bachelor_education = models.CharField(max_length=50, null=True, choices=EDUCATIONLEVEL4)
    master_doctoral_education = models.CharField(max_length=50, null=True, choices=EDUCATIONLEVEL5)
    curriculum_strands = models.CharField(max_length=150, null=True, choices=STRAND)
    undergraduate_reason = models.CharField(max_length=150, null=True, choices=REASON)

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.resident}"

    history = AuditlogHistoryField()

ARRANGEMENT = (
    ('Work From Home', 'Work From Home'),
    ('Home-based Work', 'Home-based Work'),
    ('On Job Rotation', 'On Job Rotation'),
    ('On a Mixed Arrangement', 'On a Mixed Arrangement'),
    ('On Reduced Hours', 'On Reduced Hours'),
)

EMPLOYMENT = (
    ('Permanent Job/Business', 'Permanent Job/Business'),
    ('Short Term/Seasonal Job', 'Short Term/Seasonal Job'),
    ('Worked for Different Employers', 'Worked for Different Employers'),
)

WORKER = (
    ('Private Household', 'Private Household'),
    ('Private Establishment', 'Private Establishment'),
    ('Government/Corporation', 'Government/Corporation'),
    ('Self - Employed', 'Self - Employed'),
    ('Unemployed', 'Unemployed'),
    ('Employer', 'Employer'),
    ('Family Operated Business', 'Family Operated Business'),
)

PAYMENT = (
    ('Imputed Salary', 'Imputed Salary'),
    ('Per Piece', 'Per Piece'),
    ('Per Hour', 'Per Hour'),
    ('Per Day', 'Per Day'),
    ('Monthly', 'Monthly'),
    ('Weekly', 'Weekly'),
)
class Economic(models.Model):
    specific_occupation = models.CharField(max_length=50, null=True) 
    industry_of_work = models.CharField(max_length=50, null=True) 
    working_arrangement = models.CharField(max_length=50, null=True, choices=ARRANGEMENT)
    nature_of_employment = models.CharField(max_length=50, null=True, choices=EMPLOYMENT)
    class_of_worker = models.CharField(max_length=50, null=True, choices=WORKER)
    basis_of_payment = models.CharField(max_length=50, null=True, choices=PAYMENT)

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.resident}"

    history = AuditlogHistoryField()
 

SPOT_TYPE_CHOICES = [
        ('Natural Attraction', 'Natural Attraction'),
        ('Historical/Cultural Site', 'Historical/Cultural Site'),
        ('Adventure/Outdoor Activity', 'Adventure/Outdoor Activity'),
        ('Recreational/Relaxation Spot', 'Recreational/Relaxation Spot'),
        ('EducationalInstitution', 'Educational Institution'),
        ('Food/Culinary Spot', 'Food/Culinary Spot'),
        ('Scenic View/Lookout Point', 'Scenic View/Lookout Point'),
        ('Festival/Event', 'Festival/Event'),
    ]
class TouristSpot(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(default=11.5833) 
    longitude = models.FloatField(default=124.4642) 
    photo = models.ImageField(upload_to='tourist_spot_photos/', default='path/to/default/FB_IMG_1692936618339.jpg')
    spot_type = models.CharField(max_length=50, choices=SPOT_TYPE_CHOICES, default='Natural Attraction')
    municipal = models.ForeignKey(Municipal, on_delete=models.CASCADE, null=True) 
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE, null=True) 
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    history = AuditlogHistoryField()

DOCUMENT_TYPE_CHOICES = [
    ('barangay_clearance', 'Barangay Clearance'),
    ('certificate_of_indigency', 'Certificate of Indigency'),
]

class Transaction(models.Model):
    requester = models.ForeignKey(Resident, on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    document_type = models.CharField(max_length=50, null=True, blank=True, choices=DOCUMENT_TYPE_CHOICES)
    municipal = models.ForeignKey(Municipal, on_delete=models.SET_NULL, null=True, blank=True)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Transaction #{self.id} - {self.requester.first_name} {self.requester.last_name} ({self.request_date})"

auditlog.register(CustomUser)
auditlog.register(Municipal)
auditlog.register(Barangay)
auditlog.register(Resident)
auditlog.register(Household)
auditlog.register(Education)
auditlog.register(Health)
auditlog.register(Economic)
auditlog.register(TouristSpot)


