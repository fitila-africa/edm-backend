from django.db import models
from account.models import User

class EcoSystem(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=250, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    

    @property
    def sub_ecosystem(self):
        sub = self.ecosystems.all()

        return list(map(lambda object: {
            "id":object.id,
            "name":object.name, 
            "organizations": list(map(lambda x: {"id":x.id,
                                                "name":x.name, 
                                                "company_logo_url": x.company_logo_url, "ceo_image_url":x.ceo_image_url, "state":x.state, 
                                                "sector":x.sector.name,
                                                "sub_ecosystem_sub_class":x.sub_ecosystem_sub_class,
                                                "employee" :x.num_of_employees, "funding":x.funding
                                                },object.organizations.all().filter(is_active=True).filter(is_approved=True)))
            }, sub))

    def __str__(self):
        return self.name

class SubEcosystem(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250, null=True)
    ecosystem = models.ForeignKey(EcoSystem, on_delete=models.CASCADE, related_name='ecosystems')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def organization(self):
        organization =  self.organizations.all().filter(is_active=True).filter(is_approved=True)
        data = map(lambda object: {"id":object.id,"name":object.name}, organization)
        return list(data)

class Sector(models.Model):
    name = models.CharField(max_length=250, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    

    @property
    def organization(self):
        sector = self.organizations.all().filter(is_active=True).filter(is_approved=True)

        return list(map(lambda x: {"id":x.id,
                                                "name":x.name, 
                                                "company_logo_url": x.company_logo_url, "ceo_image_url":x.ceo_image_url, "state":x.state, 
                                                "sector":x.sector.name,
                                                "employee" :x.num_of_employees,
                                                "funding":x.funding
                                                },sector))
            
    def __str__(self):
        return self.name



class Organization(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orgaizations', null=True)
    name                    = models.CharField(max_length=350)
    company_logo            = models.ImageField(null=True)
    company_logo_url        = models.CharField(max_length=200, null=True)
    num_of_employees        = models.CharField(max_length=100, null=True)
    state                   = models.CharField(max_length=150)
    address                 = models.CharField(max_length=250)
    ecosystem               = models.ForeignKey(EcoSystem, on_delete=models.CASCADE, related_name='organizations', blank =True, null=True)
    sub_ecosystem           = models.ForeignKey(SubEcosystem, on_delete=models.CASCADE, related_name='organizations', blank =True, null=True)
    sub_ecosystem_sub_class = models.CharField(max_length=200, null=True)
    sector                  = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='organizations', blank =True, null=True)
    business_level          = models.CharField(max_length=200, blank =True, null=True)
    funding                 = models.CharField(max_length=200, null=True)
    company_valuation       = models.CharField(max_length=200, null=True)
    is_startup              = models.CharField(max_length=20, blank =True, null=True)
    num_supported_business  = models.CharField(max_length=20, blank =True, null=True)
    ceo_name                = models.CharField(max_length=200, null=True)
    ceo_gender              = models.CharField(max_length=200, null=True)
    ceo_image               = models.ImageField(null=True)
    ceo_image_url           = models.CharField(max_length=200, null=True)
    website                 = models.CharField(max_length=350, blank =True, null=True)
    email                   = models.EmailField()
    phone                   = models.CharField(max_length=50)
    description             = models.TextField(null=True, blank=True)
    head_quarters           = models.CharField(max_length=350, blank =True, null=True)
    facebook                = models.CharField(max_length=350, blank =True, null=True)
    instagram               =models.CharField(max_length=350, blank =True, null=True)
    linkedin                =models.CharField(max_length=350, blank =True, null=True)
    twitter                 =models.CharField(max_length=350, blank =True, null=True)
    url_1                   =models.CharField(max_length=350, blank =True, null=True)
    url_2                   =models.CharField(max_length=350, blank =True, null=True)
    url_3                   =models.CharField(max_length=350, blank =True, null=True)
    cac_doc                 = models.CharField(max_length=350, blank =True, null=True)
    is_entrepreneur         = models.BooleanField(default=False)
    is_ecosystem            = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_approved                = models.BooleanField(default=False)
    is_declined              = models.BooleanField(default=False)
    responded               = models.BooleanField(default=False)
    date_created            = models.DateTimeField(auto_now_add=True)
    date_updated            = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    @property
    def sector_name(self):
        return self.sector.name


    @property
    def ecosystem_name(self):
        return self.ecosystem.name

    @property
    def sub_ecosystem_name(self):
        return self.sub_ecosystem.name