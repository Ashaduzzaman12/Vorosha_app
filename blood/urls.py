from django.urls import path
from . import views
from .views import register
from django.contrib.auth import views as auth_views
from .views import create_request
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('request/', create_request, name='create_request'),
    path('request/success/', TemplateView.as_view(template_name='request_success.html'), name='request_success'),
    path('responses/', views.donor_responses, name='donor_responses'),
    path('respond/<int:request_id>/', views.respond_to_request, name='respond_to_request'),
]

