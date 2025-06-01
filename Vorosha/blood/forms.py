from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    blood_group = forms.ChoiceField(choices=[
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-")
    ], required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    city_location = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 
                 'blood_group', 'date_of_birth', 'city_location')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                blood_group=self.cleaned_data['blood_group'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                city_location=self.cleaned_data['city_location']
            )
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['blood_group', 'date_of_birth', 'city_location', 'last_date_of_donation']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'last_date_of_donation': forms.DateInput(attrs={'type': 'date'}),
        }

from .models import DonationRequest

class DonationRequestForm(forms.ModelForm):
    class Meta:
        model = DonationRequest
        fields = [
            'blood_group',
            'patient_type',
            'hospital_name',
            'hospital_address',
            'contact_number',
            'additional_notes',
            'urgency'
        ]
        widgets = {
            'additional_notes': forms.Textarea(attrs={'rows': 3}),
        }
