from rest_framework import serializers
from .models import Organization, EcoSystem

class OrganizationSerializer(serializers.ModelSerializer):
    ecosystem = serializers.SlugRelatedField(slug_field='name', queryset=EcoSystem.objects.all())

    class Meta:
        model = Organization
        fields = '__all__'

class EcosystemSerializer(serializers.ModelSerializer):
    organization = serializers.ReadOnlyField()

    class Meta:
        model = EcoSystem
        fields = ('name', 'organization', 'date_created', 'date_updated')

class SubecosystemSerializer(serializers.ModelSerializer):
    organization = serializers.ReadOnlyField()

    class Meta:
        model = EcoSystem
        fields = ('name', 'ecosystem', 'organization', 'date_created', 'date_updated')