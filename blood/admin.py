from django.contrib import admin
from .models import Organization, Donor, Medical_history, DonationRequest

admin.site.register(Organization)
admin.site.register(Donor)
admin.site.register(Medical_history)
admin.site.register(DonationRequest)