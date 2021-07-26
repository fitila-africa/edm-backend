from rest_framework import serializers
from .models import Organization, EcoSystem, Sector, SubEcosystem

class EcosystemSerializer(serializers.ModelSerializer):
    sub_ecosystem = serializers.ReadOnlyField()
    num_of_organization = serializers.ReadOnlyField()
    num_of_states = serializers.ReadOnlyField()

    class Meta:
        model = EcoSystem
        fields = ('id', 'name', 'num_of_states', 'num_of_organization', 'sub_ecosystem', 'date_created', 'date_updated')

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
    file = serializers.FileField(required=True)

    class Meta:
        fields = ('file',)



class OrganizationSerializer(serializers.ModelSerializer):
    sector_name = serializers.ReadOnlyField()
    ecosystem_name = serializers.ReadOnlyField()
    sub_ecosystem_name = serializers.ReadOnlyField()

    class Meta:
        model = Organization
        fields = ['id','user','name','company_logo','company_logo_url',         'num_of_employees','state', 'address','ecosystem', 'ecosystem_name',
        'sub_ecosystem', 'sub_ecosystem_name',
        'sub_ecosystem_sub_class','sector','sector_name','business_level',
        'funding', 'company_valuation', 'is_startup', 'num_supported_business',
        'ceo_name', 'ceo_image', 'ceo_gender', 'ceo_image_url','website','email',
        'phone','description','head_quarters', 'facebook',  
        'instagram','linkedin', 'twitter', 'url_1','url_2','url_3','cac_doc','is_entrepreneur','is_ecosystem','date_created', 'date_updated']