from rest_framework import serializers
from .models import DeclineOrganization, Organization, EcoSystem, Sector, SubEcosystem, SubecosystemSubclass

class EcosystemSerializer(serializers.ModelSerializer):
    sub_ecosystem = serializers.ReadOnlyField()
    num_of_organization = serializers.ReadOnlyField()
    num_of_states = serializers.ReadOnlyField()
    num_of_sectors = serializers.ReadOnlyField()

    class Meta:
        model = EcoSystem
        fields = ('id', 'name', 'num_of_states', 'num_of_organization', 'num_of_sectors', 'sub_ecosystem', 'date_created', 'date_updated')

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

class SubecosystemSubclassSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SubecosystemSubclass
        fields = '__all__'
        
        
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    class Meta:
        fields = ('file',)



class OrganizationSerializer(serializers.ModelSerializer):
    sector_detail = serializers.ReadOnlyField()
    ecosystem_detail = serializers.ReadOnlyField()
    sub_ecosystem_detail = serializers.ReadOnlyField()
    sub_ecosystem_sub_class_detail = serializers.ReadOnlyField()
    reason_for_decline = serializers.ReadOnlyField()
    
    class Meta:
        model = Organization
        fields = ['id','user','name','company_logo','company_logo_url', 'num_of_employees','state', 'address','ecosystem', 'ecosystem_detail',
        'sub_ecosystem', 'sub_ecosystem_detail',
        'sub_ecosystem_sub_class', 'sub_ecosystem_sub_class_detail', 'sector','sector_detail','business_level', 'funding', 'funding_disbursed_for_support','company_valuation', 'num_supported_business', 'ceo_name', 'ceo_image', 'ceo_gender', 'ceo_image_url','website','email',
        'phone','description','head_quarters', 'facebook',  
        'instagram','linkedin', 'twitter', 'url_1','url_2','url_3','cac_doc', 'no_of_jobs','is_entrepreneur','is_ecosystem', 'reason_for_decline','date_created', 'date_updated']
        
    def create(self, validated_data, user):
        ecosystem_ = validated_data.pop('ecosystem')
        sub_ecosystem_ =  validated_data.pop('sub_ecosystem')
        sub_ecosystem_sub_class_ = validated_data.pop('sub_ecosystem_sub_class')
        sector_ = validated_data.pop('sector')
    
        org = Organization.objects.create(**validated_data, user=user)
        org.ecosystem.set(ecosystem_)
        org.sub_ecosystem.set(sub_ecosystem_)
        org.sub_ecosystem_sub_class.set(sub_ecosystem_sub_class_)
        org.sector=sector_
        org.save()
        
        return org
    
   
    
class DeclineOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclineOrganization
        fields = '__all__'
        
        
        