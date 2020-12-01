from django.urls import path

from .views import (
    CompanyDetailView,
    CompanyFocalCreateView,
    CompanyFocalDeleteView,
    CompanyListView,
    CompanyRtvCreateView,
    CompanyRtvDeleteView,
    FocalCreateView,
    FocalDetailView,
    FocalEditView,
    FocalListView,
    RtvCreateView,
    RtvDetailView,
    RtvEditView,
    RtvListView,
    StoreCreateView,
    StoreDetailView,
    StoreEditView,
    StorePublicExportView,
)

app_name = "comercial"

urlpatterns = [
    # Company
    path("distribuidores/", CompanyListView.as_view(), name="companies"),
    path("distribuidores/<int:pk>/", CompanyDetailView.as_view(), name="company"),
    path(
        "distribuidores/<int:company>/focal/atribuir",
        CompanyFocalCreateView.as_view(),
        name="focal_assign",
    ),
    path(
        "distribuidores/<int:company>/focal/<int:focal>/desatribuir",
        CompanyFocalDeleteView.as_view(),
        name="focal_unassign",
    ),
    path(
        "distribuidores/<int:company>/rtv/atribuir",
        CompanyRtvCreateView.as_view(),
        name="rtv_assign",
    ),
    path(
        "distribuidores/<int:company>/rtv/<int:rtv>/desatribuir",
        CompanyRtvDeleteView.as_view(),
        name="rtv_unassign",
    ),
    # Store
    path(
        "distribuidores/<int:company>/filial/<int:pk>/",
        StoreDetailView.as_view(),
        name="store",
    ),
    path(
        "distribuidores/<int:company>/filial/adicionar",
        StoreCreateView.as_view(),
        name="store_create",
    ),
    path(
        "distribuidores/<int:company>/filial/<int:pk>/editar",
        StoreEditView.as_view(),
        name="store_edit",
    ),
    path(
        "distribuidores/<int:company>/filial/export",
        StorePublicExportView.as_view(),
        name="store_export",
    ),
    # Focal
    path("responsaveis/", FocalListView.as_view(), name="focals"),
    path("responsaveis/<int:pk>/", FocalDetailView.as_view(), name="focal"),
    path("responsaveis/adicionar", FocalCreateView.as_view(), name="focal_create"),
    path("responsaveis/<int:pk>/editar", FocalEditView.as_view(), name="focal_edit"),
    # RTV
    path("rtvs/", RtvListView.as_view(), name="rtvs"),
    path("rtvs/<int:pk>/", RtvDetailView.as_view(), name="rtv"),
    path("rtvs/adicionar", RtvCreateView.as_view(), name="rtv_create"),
    path("rtvs/<int:pk>/editar", RtvEditView.as_view(), name="rtv_edit"),
]
