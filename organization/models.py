from django.db import models
from account.models import User

class EcoSystem(models.Model):
    name = models.CharField(max_length=250, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def organization(self):
        organization = self.organizations.all()

        data = map(lambda object: {"id":object.id,"name":object.name,}, organization)
        return list(data)

    @property
    def sub_ecosystem(self):
        sub = self.ecosystems.all()

        return list(map(lambda object: {"id":object.id,"name":object.name,}, sub))

    def __str__(self):
        return self.name

class SubEcosystem(models.Model):
    name = models.CharField(max_length=250)
    ecosystem = models.ForeignKey(EcoSystem, on_delete=models.CASCADE, related_name='ecosystems')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def organization(self):
        organization = self.sub_ecosystem.all()
        data = map(lambda object: {"id":object.id,"name":object.name,}, organization)
        return list(data)

    

class Organization(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orgaizations', null=True)
    name = models.CharField(max_length=350)
    state = models.CharField(max_length=150)
    # local_gov = models.CharField(max_length=200)
    address = models.CharField(max_length=250)
    ecosystem = models.ForeignKey(EcoSystem, on_delete=models.CASCADE, related_name='organizations', null=True)
    sub_ecosystem = models.ForeignKey(SubEcosystem, on_delete=models.CASCADE, related_name='sub_ecosystem', null=True)
    sector = models.CharField(max_length=200, null=True)
    business_level = models.CharField(max_length=200, null=True)
    is_startup = models.CharField(max_length=20, null=True)
    num_supported_business = models.IntegerField(null=True)
    ceo_name = models.CharField(max_length=200)
    website = models.URLField(max_length=350, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    facebook = models.URLField(max_length=350, null=True)
    instagram =models.URLField(max_length=350, null=True)
    linkedin =models.URLField(max_length=350, null=True)
    twitter =models.URLField(max_length=350, null=True)
    url_1 =models.URLField(max_length=350, null=True)
    url_2 =models.URLField(max_length=350, null=True)
    url_3 =models.URLField(max_length=350, null=True)
    cac_doc = models.CharField(max_length=350, null=True)
    gov_id = models.CharField(max_length=350, null=True)
    is_entrepreneur = models.BooleanField(default=False)
    is_ecosystem = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name