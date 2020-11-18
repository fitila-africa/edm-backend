from organization.models import Organization
from django.contrib import admin
from .models import EcoSystem, Organization

# Register your models here.
admin.site.register(Organization)
admin.site.register(EcoSystem)