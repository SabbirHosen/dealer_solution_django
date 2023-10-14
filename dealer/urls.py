from django.urls import path
from . import views

app_name = "dealer"

urlpatterns = [
    path("", views.DealerHome.as_view(), name="home"),
    path("dealer-training/", views.DealerTraining.as_view(), name="dealer-training"),
]
