from .models import *

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.gis import forms
from django.forms import ModelForm, inlineformset_factory

class UploadClearanceForm(forms.Form):
    clearance_file = forms.FileField(label='Upload Word File')

class UploadIndigencyForm(forms.Form):
    indigency_file = forms.FileField(label='Upload Word File')

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = '__all__'  # Include all fields from the Resident model

class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = '__all__'
        widgets = {
            'municipal': forms.HiddenInput(),  
            'barangay': forms.HiddenInput(),  
        }

class HealthForm(forms.ModelForm):
    class Meta:
        model = Health
        fields = '__all__'  # Include all fields from the Health model

class EconomicForm(forms.ModelForm):
    class Meta:
        model = Economic
        fields = '__all__'  # Include all fields from the Economic model

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'  # Include all fields from the Education model
        
class MunicipalForm(ModelForm):
    class Meta:
        model = Municipal
        fields = '__all__'

class BarangayForm(forms.ModelForm):
    municipal = forms.ModelChoiceField(queryset=Municipal.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Barangay
        fields = ['name', 'municipal']

class MunicipalSelectForm(forms.Form):
    municipal_choices = [(municipal.id, municipal.name) for municipal in Municipal.objects.all()]
    municipal = forms.ChoiceField(choices=[('', 'Select Municipal')] + municipal_choices, required=False)

class BarangaySelectForm(forms.Form):
    barangay_choices = [(barangay.id, barangay.name) for barangay in Barangay.objects.all()]
    barangay = forms.ChoiceField(choices=[('', 'Select Barangay')] + barangay_choices, required=False)

class SuperUserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)

        # Filter user types based on the desired types
        self.fields['user_type'].choices = [ut for ut in CustomUser.USER_TYPES if ut[0] in ['provincial_admin']]

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'user_type', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user

class ProvincialUserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)

        # Filter user types based on the desired types
        self.fields['user_type'].choices = [ut for ut in CustomUser.USER_TYPES if ut[0] in ['municipal_admin']]

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'user_type', 'municipal', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-select'}),
            'municipal': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user

class MunicipalUserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'user_type', 'barangay', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-select'}),
            'barangay': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)

        # Set the initial queryset for barangay based on the municipal of the user
        if user and user.municipal:
            self.fields['barangay'].queryset = Barangay.objects.filter(municipal=user.municipal)
            
        # Filter user types based on the desired types
        self.fields['user_type'].choices = [ut for ut in CustomUser.USER_TYPES if ut[0] in ['tourist_staff', 'barangay_staff', 'barangay_admin']]
        
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False  
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'user_type', 'barangay', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-select'}),
            'barangay': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

    def save(self, commit=True):
        user = self.instance
        user.username = self.cleaned_data['username']
        user.user_type = self.cleaned_data['user_type']
        user.barangay = self.cleaned_data['barangay']
        password = self.cleaned_data['password']
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


# class UserEditForm(forms.ModelForm):
#     current_password = forms.CharField(
#         label='Current Password',
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         required=False
#     )
#     new_password1 = forms.CharField(
#         label='New Password',
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         required=False
#     )
#     new_password2 = forms.CharField(
#         label='Confirm New Password',
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         required=False
#     )

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'user_type', 'municipal', 'barangay')
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'user_type': forms.Select(attrs={'class': 'form-select'}),
#             'municipal': forms.Select(attrs={'class': 'form-select'}),
#             'barangay': forms.Select(attrs={'class': 'form-select'}),
#         }

#     def clean_current_password(self):
#         current_password = self.cleaned_data.get('current_password')
#         if current_password and not self.instance.check_password(current_password):
#             raise forms.ValidationError('Invalid current password.')
#         return current_password

#     def clean(self):
#         cleaned_data = super().clean()
#         new_password1 = cleaned_data.get('new_password1')
#         new_password2 = cleaned_data.get('new_password2')
#         if new_password1 or new_password2:
#             if not new_password1 or not new_password2:
#                 raise forms.ValidationError("Both new password fields must be filled.")
#             elif new_password1 != new_password2:
#                 raise forms.ValidationError("The new passwords don't match.")
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         current_password = self.cleaned_data.get('current_password')
#         new_password1 = self.cleaned_data.get('new_password1')
#         new_password2 = self.cleaned_data.get('new_password2')

#         if new_password1 and new_password2:
#             if not user.check_password(current_password):
#                 raise forms.ValidationError('Invalid current password.')
#             elif new_password1 != new_password2:
#                 raise forms.ValidationError("The new passwords don't match.")
#             else:
#                 user.set_password(new_password1)

#         if commit:
#             user.save()
#         return user

class TouristSpotAdminForm(forms.ModelForm):
    class Meta:
        model = TouristSpot
        fields = '__all__'


class HouseholdAdminForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = '__all__'

