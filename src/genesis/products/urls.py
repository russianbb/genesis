from django.urls import path

from .views import (
    CompanyProductCreateView,
    CompanyProductDetailView,
    CompanyProductEditView,
    CompanyProductFilterView,
    CompanyProductListView,
    OnixProductDetailView,
    OnixProductListView,
    SyngentaProductDetailView,
    SyngentaProductListView,
)

app_name = "products"


urlpatterns = [
    # Onix
    path("produtos/onix/", OnixProductListView.as_view(), name="onix_list",),
    path("produtos/onix/<int:pk>/", OnixProductDetailView.as_view(), name="onix",),
    # Syngenta
    path(
        "produtos/syngenta/", SyngentaProductListView.as_view(), name="syngenta_list",
    ),
    path(
        "produtos/syngenta/<str:agicode>/",
        SyngentaProductDetailView.as_view(),
        name="syngenta",
    ),
    # Company
    path(
        "produtos/distribuidores/",
        CompanyProductFilterView.as_view(),
        name="company_filter",
    ),
    path(
        "produtos/distribuidores/<int:code_sap>",
        CompanyProductListView.as_view(),
        name="company_list",
    ),
    path(
        "produtos/distribuidores/<int:code_sap>/produto/<int:pk>",
        CompanyProductDetailView.as_view(),
        name="company",
    ),
    path(
        "produtos/distribuidores/<int:code_sap>/produto/<int:pk>/editar",
        CompanyProductEditView.as_view(),
        name="company_edit",
    ),
    path(
        "produtos/distribuidores/<int:code_sap>/",
        CompanyProductCreateView.as_view(),
        name="company_create",
    ),
]
