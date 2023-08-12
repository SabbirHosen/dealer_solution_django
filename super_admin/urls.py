from django.urls import path
from . import views

app_name = 'super_admin'

urlpatterns = [
    # path('help-support/', views.HelpSupportView.as_view(), name='help-support'),
    # path('help-support-list', views.HelpSupportListView.as_view(), name='help-support-list'),
    path('request-join/', views.RequestToJoin.as_view(), name='request-join'),
]
