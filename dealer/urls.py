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
        "dealer-edit-product-/<int:pk>",
        views.EditProduct.as_view(),
        name="dealer-edit-product",
    ),
    path(
        "bulk-product-upload/",
        views.ProductBulkUpload.as_view(),
        name="bulk-product-upload",
    ),
    path("product-stock/", views.ProductListView.as_view(), name="product-stock"),
    path("dsr-list/", views.DSRList.as_view(), name="dsr-list"),
    path("dsr-request/", views.DSRRequest.as_view(), name="dsr-request"),
    path("dsr-details/<int:pk>", views.DSRDetails.as_view(), name="dsr-details"),
    path(
        "dsr-product-van-load/<int:pk>",
        views.DSRProductVanLoad.as_view(),
        name="dsr-product-van-load",
    ),
    path(
        "dsr-return-product/<int:pk>",
        views.DSRReturnProduct.as_view(),
        name="dsr-return-product",
    ),
    path(
        "dsr-product-wallet/<int:pk>",
        views.DSRProductWalletView.as_view(),
        name="dsr-product-wallet",
    ),
    path(
        "dsr-calculation/<int:pk>",
        views.DSRCalculationView.as_view(),
        name="dsr-calculation",
    ),
    path(
        "dsr-calculation-individual/<int:pk>",
        views.DSRIndividualCalculationView.as_view(),
        name="dsr-calculation-individual",
    ),
    #   API
    path(
        "dealer-product-upload/product-info-api/",
        views.ProductListViewForAPI.as_view(),
        name="product-for-api",
    ),
    path(
        "dsr-product-van-load/<int:pk>/dsr/product-list/",
        views.DSRProductForAPI.as_view(),
        name="dsr-product-for-api",
    ),
    path(
        "dsr-return-product/<int:pk>/dsr/product-list/",
        views.DSRProductForAPI.as_view(),
        name="dsr-product-for-api",
    ),
]
