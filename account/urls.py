from account.views import get_user
from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [

    #users
    path('add_user/', views.add_user),
    path('get_user/', views.get_user),
    path('user/<int:pk>', views.user_detail),

    #user login
    path('auth/', views.user_login),

]