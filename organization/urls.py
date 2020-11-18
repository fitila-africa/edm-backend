from organization.views import ecosystem
from django.urls import path
from organization import views

app_name = 'organization'

urlpatterns = [

   path('organizations/', views.organizations),
   path('organizations/<int:pk>', views.organization_detail),
   path('ecosystem/', views.ecosystem),
   path('ecosystem/<int:pk>', views.ecosystem_detail)

]