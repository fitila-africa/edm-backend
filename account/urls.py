from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'account'

urlpatterns = [

    #users
    path('add_user/', views.add_user),
    path('add_admin/', views.add_admin),
    path('get_user/', views.get_user),
    path('user/<int:pk>', views.user_detail),

    #user login
    path('auth/', views.user_login),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]