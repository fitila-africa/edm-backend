from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EcoSystem(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=250, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    

    @property
    def sub_ecosystem(self):
        sub = self.ecosystems.all()
        

        return list(map(lambda object: {
            "id":object.id,
            "name":object.name, 
            "organizations": list(map(lambda x: x.org_dict(), object.organizations.filter(is_active=True, is_approved=True)))
            }, sub))
        
    @property
    def num_of_organization(self):
        return self.organizations.filter(is_active=True, is_approved=True).count()
    
    @property
    def num_of_states(self):
        return self.organizations.filter(is_active=True, is_approved=True).values('state').distinct().count()
    
    @property
    def num_of_sectors(self):
        return self.organizations.filter(is_active=True, is_approved=True).values('sector').distinct().count()
    
    def __str__(self):
        return self.name
    
    def delete(self):
        self.is_active = False
        self.save()
        return 

class SubEcosystem(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250, null=True)
    ecosystem = models.ForeignKey(EcoSystem, on_delete=models.CASCADE, related_name='ecosystems')
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def organization(self):
        sub_ecosystem_organization =  self.organizations.filter(is_active=True, is_approved=True)
        return list(map(lambda x: x.org_dict() ,sub_ecosystem_organization))
    
    def delete(self):
        self.is_active = False
        self.save()
        return 
    
class SubecosystemSubclass(models.Model):
    name = models.CharField(max_length=250)
    sub_ecosystem = models.ForeignKey(SubEcosystem, on_delete=models.CASCADE, related_name='sub_class')
    ecosystem = models.ForeignKey(EcoSystem, on_delete=models.CASCADE, related_name='sub_class')
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    
    def delete(self):
        self.is_active = False
        self.save()
        return 

class Sector(models.Model):
    name = models.CharField(max_length=250, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    

    @property
    def organization(self):
        sector_org = self.organizations.filter(is_active=True, is_approved=True)

        return list(map(lambda x: x.org_dict() ,sector_org))
            
    def __str__(self):
        return self.name
    
    def delete(self):
        self.is_active = False
        self.save()
        return 



class Organization(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='organizations', null=True)
    name                    = models.CharField(max_length=350)
    company_logo            = models.ImageField(null=True)
    company_logo_url        = models.CharField(max_length=200, null=True)
    num_of_employees        = models.CharField(max_length=100, null=True)
    state                   = models.CharField(max_length=150)
    address                 = models.CharField(max_length=250)
    ecosystem               = models.ForeignKey(EcoSystem, on_delete=models.CASCADE, related_name='organizations', blank =True, null=True)
    sub_ecosystem           = models.ForeignKey(SubEcosystem, on_delete=models.CASCADE, related_name='organizations', blank =True, null=True)
    sub_ecosystem_sub_class = models.ForeignKey(SubecosystemSubclass, on_delete=models.CASCADE, related_name='organizations', blank =True, null=True)
    sector                  = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='organizations', blank =True, null=True)
    business_level          = models.CharField(max_length=200, blank =True, null=True)
    funding                 = models.IntegerField(default=0)
    funding_disbursed_for_support = models.IntegerField(default=0)
    company_valuation       = models.CharField(max_length=200, null=True)
    # is_startup              = models.CharField(max_length=20, blank =True, null=True)
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
    no_of_jobs              = models.IntegerField(default=0, blank =True, null=True)
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
    
    @property
    def sub_ecosystem_sub_class_name(self):
        return self.sub_ecosystem_sub_class.name
    
    @property
    def reason_for_decline(self):
        reason = self.declined.all().last()
        if reason:
            return reason.reason
        return ""
    
    def delete(self):
        self.is_active = False
        self.save()
        return 
    
    def org_dict(self):
        
        return {"id": self.id,
          "user": self.user.id if self.user else "",
          "name": self.name,
          "company_logo": self.company_logo if self.company_logo else "",
          "company_logo_url": self.company_logo_url,
          "num_of_employees": self.num_of_employees,
          "state": self.state,
          "address": self.address,
          "ecosystem" : self.ecosystem.id if self.ecosystem else "",
          "ecosystem_name": self.ecosystem_name if self.ecosystem else "",
          "sub_ecosystem":self.sub_ecosystem.id if self.sub_ecosystem else "",
          "sub_ecosystem_name": self.sub_ecosystem_name if self.sub_ecosystem else "",
          "sub_ecosystem_sub_class":self.sub_ecosystem_sub_class.id if self.sub_ecosystem_sub_class else "",
          "sub_ecosystem_sub_class_name": self.sub_ecosystem_sub_class_name if self.sub_ecosystem_sub_class else "",
          "sector":self.sector.id if self.sector else "",
          "sector_name": self.sector_name if self.sector else "",
          "business_level": self.business_level,
          "funding": self.funding,
          "funding_disbursed_for_support": self.funding_disbursed_for_support,
          "company_valuation": self.company_valuation,
        #   "is_startup": self.is_startup,
          "num_supported_business": self.num_supported_business,
          "ceo_name": self.ceo_name,
          "ceo_gender": self.ceo_gender,
          "ceo_image":self.ceo_image if self.ceo_image else "",
          "ceo_image_url": self.ceo_image_url,
          "website": self.website,
          "email":self.email,
          "phone": self.phone,
          "description":self.description,
          "head_quarters": self.head_quarters,
          "facebook":self.facebook,
          "instagram": self.instagram,
          "linkedin": self.linkedin,
          "twitter": self.twitter,
          "url_1": self.url_1,
          "url_2": self.url_2,
          "url_3": self.url_3,
          "cac_doc": self.cac_doc,
          "no_of_jobs":self.no_of_jobs,
          "reason_for_decline" : self.reason_for_decline,
          "is_entrepreneur": self.is_entrepreneur,
          "is_ecosystem": self.is_ecosystem,
          "is_active": self.is_active,
          "is_approved": self.is_approved,
          "is_declined": self.is_declined,
          'responded' : self.responded,
          "date_created": self.date_created,
          "date_updated": self.date_updated}
        
        
        
class DeclineOrganization(models.Model):
    admin = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    reason = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, related_name='declined', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def delete(self):
        self.is_active=False
        self.save()