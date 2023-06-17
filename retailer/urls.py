from django.urls import path, include
from . import views
app_name = 'retailer'

urlpatterns = [
    path("", views.RetailerIndex.as_view(), name='retailer-home'),
    path('buy-sell/', views.BuySell.as_view(), name='buy-sell'),
    path('retailer-expenses/', views.RetailerExpense.as_view(), name='retailer-expenses'),
    path('retailer-dues/', views.RetailerDues.as_view(), name='retailer-dues'),
    path('customer-dues-details/<int:expense_id>/', views.CustomerDuesDetails.as_view(), name='customer-dues-details'),
    path('api/customer-info/', views.api_customer_info, name='customer-info-api'),
    path('retailer-business-status/api/<str:status>/<str:time_period>', views.RetailerBusinessStatusData.as_view(), name='retailer-business-status-data-api'),
    path('retailer-collection/', views.RetailerCollection.as_view(), name='retailer-collection'),
    path('retailer-business-status/', views.RetailerBusinessStatus.as_view(), name='retailer-business-status'),

]
