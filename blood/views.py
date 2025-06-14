from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .forms import RegistrationForm
from django import forms
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .forms import DonationRequestForm
from .models import DonationRequest
from .models import DonationResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, DonationRequest, DonationResponse
from .forms import RegistrationForm, ProfileForm, DonationRequestForm

def home(request):
    return render(request,'home.html',{})

def about(request):
    return render(request,'about.html',{})


def logout_user(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect('home')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # This saves User and UserProfile
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']  # Change from email to username
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def profile_view(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'form': form,
        'user': request.user,
        'profile': profile,
    })

def create_request(request):
    if request.method == 'POST':
        form = DonationRequestForm(request.POST)
        if form.is_valid():
            donation_request = form.save(commit=False)
            donation_request.requester = request.user
            donation_request.save()
            return redirect('request_success')  # Create this URL
    else:
        form = DonationRequestForm()
    
    return render(request, 'request.html', {'form': form})



@login_required
def respond_to_request(request, request_id):
    blood_request = get_object_or_404(DonationRequest, id=request_id)
    
    if request.method == 'POST':
        message = request.POST.get('message', '')
        DonationResponse.objects.create(
            request=blood_request,
            donor=request.user,
            message=message
        )
        messages.success(request, 'Your response has been submitted!')
        return redirect('donor_responses')
    
    return redirect('donor_responses')

@login_required
def donor_responses(request):
    active_requests = DonationRequest.objects.filter(
        is_fulfilled=False
    ).exclude(
        requester=request.user
    ).order_by('-urgency', '-created_at')
    
    your_responses = DonationResponse.objects.filter(
        donor=request.user
    ).order_by('-response_date')
    
    return render(request, 'donor_responses.html', {
        'active_requests': active_requests,
        'your_responses': your_responses
    })