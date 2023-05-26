from django.urls import path
from . import views
app_name = 'authentication'

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
]
