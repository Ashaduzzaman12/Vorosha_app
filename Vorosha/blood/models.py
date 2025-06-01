from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3)
    date_of_birth = models.DateField()
    city_location = models.CharField(max_length=100)
    last_date_of_donation = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username



class Donor(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    blood_group = models.CharField(max_length=3, choices=[
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-")
    ])
    
    date_of_birth = models.DateField()
    city_location = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Organization(models.Model): 
    orga_id=models.CharField(max_length=10)
    orga_name=models.CharField(max_length=50)
    orga_loc=models.CharField(max_length=120)
    contact_info=models.CharField(max_length=12)

    def _str_(self):
         return self.orga_id




class Medical_history(models.Model): 
     user_id=models.ForeignKey(Donor,on_delete=models.CASCADE)
     phone=models.CharField(max_length=11)
     email=models.EmailField(max_length=30)
     password=models.CharField(max_length=100)
     location=models.CharField(max_length=100)


     def _str_(self):
        return self.phone

class DonationRequest(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    PATIENT_TYPES = [
        ('Child', 'Child'),
        ('Adult', 'Adult'),
        ('Elderly', 'Elderly'),
        ('Pregnant Woman', 'Pregnant Woman'),
        ('Accident Victim', 'Accident Victim'),
        ('Surgery Patient', 'Surgery Patient'),
    ]
    
    URGENCY_LEVELS = [
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
        ('Critical', 'Critical'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    patient_type = models.CharField(max_length=20, choices=PATIENT_TYPES)
    hospital_name = models.CharField(max_length=100)
    hospital_address = models.TextField()
    contact_number = models.CharField(max_length=15)
    additional_notes = models.TextField(blank=True, null=True)
    urgency = models.CharField(max_length=10, choices=URGENCY_LEVELS, default='Normal')
    created_at = models.DateTimeField(auto_now_add=True)
    is_fulfilled = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.blood_group} request by {self.requester.username}"
    
class DonationResponse(models.Model):
    request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE)
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    response_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.donor.username}'s response to {self.request.blood_group} request"