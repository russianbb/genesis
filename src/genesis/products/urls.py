from django.urls import path

from .views import (
    CompanyProductDetailView,
    CompanyProductListView,
    OnixProductDetailView,
    OnixProductListView,
    SyngentaProductDetailView,
    SyngentaProductListView,
)

app_name = "products"


urlpatterns = [
    # Onix
    path("produtos/onix/", OnixProductListView.as_view(), name="onix_list"),
    path("produtos/onix/<int:pk>/", OnixProductDetailView.as_view(), name="onix"),
    # Syngenta
    path("produtos/syngenta/", SyngentaProductListView.as_view(), name="syngenta_list"),
    path(
        "produtos/syngenta/<str:agicode>/",
        SyngentaProductDetailView.as_view(),
        name="syngenta",
    ),
    # Company
    path(
        "produtos/distribuidor/", CompanyProductListView.as_view(), name="company_list"
    ),
    path(
        "produtos/distribuidor/<int:pk>/",
        CompanyProductDetailView.as_view(),
        name="company",
    ),
]
