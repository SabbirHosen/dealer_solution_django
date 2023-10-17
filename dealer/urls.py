from django.urls import path
from . import views

app_name = "dealer"


urlpatterns = [
    path("", views.DealerHome.as_view(), name="home"),
    path(
        "dealer-privacy-policy/",
        views.DealerPrivacyPolicy.as_view(),
        name="dealer-privacy-policy",
    ),
    path("dealer-training/", views.DealerTraining.as_view(), name="dealer-training"),
    path("dealer-expenses/", views.DealerExpenses.as_view(), name="dealer-expenses"),
    path(
        "dealer-product-upload/",
        views.ProductUpload.as_view(),
        name="dealer-product-upload",
    ),
    path(
        "dealer-new-product-upload/",
        views.NewProductUpload.as_view(),
        name="dealer-new-product-upload",
    ),
    path(
        "bulk-product-upload/",
        views.ProductBulkUpload.as_view(),
        name="bulk-product-upload",
    ),
    #   API
    path(
        "bulk-product-upload/product-info-api/",
        views.ProductListViewForAPI.as_view(),
        name="product-for-api",
    ),
]
