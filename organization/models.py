from typing import Tuple
from django.db import models
from django.utils import tree
from account.models import User

class EcoSystem(models.Model):
    name = models.CharField(max_length=250, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def organization(self):
        organization = Organization.objects.filter(ecosystem= self.pk)

        data = map(lambda object: {"id":object.id,"name":object.name,}, organization)
        return list(data)

    def __str__(self):
        return self.name


class Organization(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orgaizations', null=True)
    name = models.CharField(max_length=350)
    town = models.CharField(max_length=200)
    state = models.CharField(max_length=150)
    local_gov = models.CharField(max_length=200)
    street_num = models.CharField(max_length=50, null=True)
    street_name = models.CharField(max_length=250)
    ecosystem = models.ForeignKey(EcoSystem, on_delete=models.CASCADE, related_name='organizations')
    business_sector = models.CharField(max_length=200, null=True)
    num_supported_business = models.IntegerField(null=True)
    website = models.URLField(max_length=350, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    facebook = models.URLField(max_length=350, null=True)
    instagram =models.URLField(max_length=350, null=True)
    linkedin =models.URLField(max_length=350, null=True)
    twitter =models.URLField(max_length=350, null=True)
    cac_doc = models.FileField(upload_to='documents/', null=True)
    cac_doc_url = models.CharField(max_length=350, null=True)
    gov_id = models.FileField(upload_to='documents/', null=True)
    gov_id_url = models.CharField(max_length=350, null=True)
    is_entrepreneur = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name