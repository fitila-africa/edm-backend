from rest_framework import serializers
from .models import User
# from django.contrib.auth.hashers import check_password
class UserSerializer(serializers.ModelSerializer):
    user_organization = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'is_admin', 'password', 'date_joined', 'user_organization']
        
        

class ChangePasswordSerializer(serializers.Serializer):
    old_password  = serializers.CharField(max_length=200)
    new_password  = serializers.CharField(max_length=200)
    confirm_password  = serializers.CharField(max_length=200)
    
    
    