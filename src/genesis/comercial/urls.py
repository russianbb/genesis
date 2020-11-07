from django.urls import path

from .views import (
    CompanyDetailView,
    CompanyListView,
    FocalCreateView,
    FocalDetailView,
    FocalListView,
    RtvListView,
    StoreCreateView,
    StoreDetailView,
    StoreEditView,
)

app_name = "comercial"

urlpatterns = [
    path("distribuidores/", CompanyListView.as_view(), name="companies"),
    path("distribuidores/<int:pk>/", CompanyDetailView.as_view(), name="company"),
    #
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
    #
    path("responsaveis/", FocalListView.as_view(), name="focals"),
    path("responsaveis/<int:pk>/", FocalDetailView.as_view(), name="focal"),
    path("responsaveis/adicionar", FocalCreateView.as_view(), name="focal_create"),
    #
    path("rtvs/", RtvListView.as_view(), name="rtvs"),
]
