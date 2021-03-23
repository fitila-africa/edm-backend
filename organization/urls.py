from organization.views import ecosystem
from django.urls import path
from organization import views

app_name = 'organization'

urlpatterns = [

   path('organizations/', views.organizations),
   path('organizations/pending', views.unapproved_organizations),
   path('add_organization/', views.add_organization),
   path('organizations/<int:pk>', views.organization_detail),
   path('ecosystem/', views.ecosystem),
   path('ecosystem/<int:pk>', views.ecosystem_detail),
   path('sub_ecosystem/', views.sub_ecosystem),
   path('sub_ecosystem/<int:pk>', views.sub_ecosystem_detail),
   path('sector/', views.sector),
   path('sector/<int:pk>', views.sector_detail),
   path('organizations/by_state/', views.state),
   path('organizations/upload_organizations/', views.upload_csv),

]