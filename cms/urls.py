from django.urls import path
from . import views

urlpatterns = [
    path('faqs/', views.faq),
    path('faqs/<int:faq_id>/', views.faq_detail)
]
