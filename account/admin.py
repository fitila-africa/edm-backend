from django.contrib import admin
from .models import User, OTP
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'is_active', 'is_staff','is_admin','is_superuser', 'date_joined' ]
    list_editable = [ 'is_active', 'is_staff','is_admin','is_superuser', ]
    
    
admin.site.register(OTP)