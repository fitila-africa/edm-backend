from rest_framework import serializers
from .models import *

class AboutUsContentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AboutUsContent
        fields = '__all__'