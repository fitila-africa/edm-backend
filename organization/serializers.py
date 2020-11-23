from rest_framework import serializers
from .models import Organization, EcoSystem, SubEcosystem

class OrganizationSerializer(serializers.ModelSerializer):
    ecosystem = serializers.SlugRelatedField(slug_field='name', queryset=EcoSystem.objects.all())

    class Meta:
        model = Organization
        fields = '__all__'

class EcosystemSerializer(serializers.ModelSerializer):
    sub_ecosystem = serializers.ReadOnlyField()
    organization = serializers.ReadOnlyField()

    class Meta:
        model = EcoSystem
        fields = ('name', 'sub_ecosystem', 'organization', 'date_created', 'date_updated')

class SubecosystemSerializer(serializers.ModelSerializer):
    organization = serializers.ReadOnlyField()

    class Meta:
        model = SubEcosystem
        fields = ('name', 'ecosystem', 'organization', 'date_created', 'date_updated')