from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken 

class UserSerializer(serializers.ModelSerializer):
    user_organization = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'is_admin', 'password', 'date_joined', 'user_organization']
        
        

class ChangePasswordSerializer(serializers.Serializer):
    old_password  = serializers.CharField(max_length=200)
    new_password  = serializers.CharField(max_length=200)
    confirm_password  = serializers.CharField(max_length=200)
    
    
    def check_pass(self):
        """ checks if both passwords are the same """
        if self.validated_data['new_password'] != self.validated_data['confirm_password']:
            raise serializers.ValidationError({"error":"Please enter matching passwords"})
        return True
            
        
    


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')