from rest_framework import serializers
from .models import Organization, EcoSystem, Sector, SubEcosystem

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'

class EcosystemSerializer(serializers.ModelSerializer):
    sub_ecosystem = serializers.ReadOnlyField()

    class Meta:
        model = EcoSystem
        fields = ('id', 'name', 'sub_ecosystem', 'date_created', 'date_updated')

class SubecosystemSerializer(serializers.ModelSerializer):
    organization = serializers.ReadOnlyField()

    class Meta:
        model = SubEcosystem
        fields = ('id', 'name', 'ecosystem', 'organization', 'date_created', 'date_updated')

class SectorSerializer(serializers.ModelSerializer):
    organization = serializers.ReadOnlyField()

    class Meta:
        model = Sector
        fields = ('id', 'name', 'organization', 'date_created', 'date_updated')

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)