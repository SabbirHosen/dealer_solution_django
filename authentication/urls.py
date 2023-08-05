from django.urls import path
from . import views
app_name = 'authentication'

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-user/', views.CreateUser.as_view(), name='create-user'),
    path('edit-user-profile/', views.EditUserProfile.as_view(), name='edit-user-profile'),
    path('pin-change/', views.ResetPin.as_view(), name='pin-change'),
]
