from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='home'),
]
