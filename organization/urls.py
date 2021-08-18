from django.urls import path
from organization import views

app_name = 'organization'

urlpatterns = [

   path('organizations/', views.organizations),
   path('organizations/pending/', views.pending_organizations),
   path('organizations/approve/<int:org_id>/', views.approve_org),
   path('organizations/decline/<int:org_id>/', views.reject_org),
   path('organizations/rejected/', views.rejected_org),
   path('organizations/<int:pk>', views.organization_detail),
   path('ecosystem/', views.ecosystem),
   path('ecosystem/<int:pk>', views.ecosystem_detail),
   path('sub_ecosystem/', views.sub_ecosystem),
   path('sub_ecosystem/<int:pk>', views.sub_ecosystem_detail),
   path('sector/', views.sector),
   path('sector/<int:pk>', views.sector_detail),
   path('subclass/', views.subclass),
   path('subclass/<int:pk>', views.subclass_detail),
   path('organizations/by_state/', views.state),
   path('organizations/upload_organizations/', views.upload_csv),

]