from rest_framework import serializers
from .models import *

# class AboutUsContentSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = None
#         fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FAQ
        fields = '__all__'