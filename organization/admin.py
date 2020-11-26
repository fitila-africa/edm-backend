from organization.models import Organization
from django.contrib import admin
from .models import EcoSystem, Organization

# Register your models here.
admin.site.register(EcoSystem)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_editable = ['is_entrepreneur', 'is_ecosystem', 'is_active']