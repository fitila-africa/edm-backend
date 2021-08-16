from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'account'

urlpatterns = [

    #users
    path('user/add_user/', views.add_user),
    path('user/add_admin/', views.add_admin),
    path('user/all_users/', views.get_user),
    path('user/profile/', views.user_detail),

    #user login
    path('auth/', views.user_login),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]