from django.urls import path

from .views import (
    CompanyDetailView,
    CompanyListView,
    FocalListView,
    RtvListView,
    StoreDetailView,
)

app_name = "comercial"

urlpatterns = [
    path("distribuidores/", CompanyListView.as_view(), name="companies"),
    path("distribuidores/<int:pk>/", CompanyDetailView.as_view(), name="company"),
    path("filial/<int:pk>/", StoreDetailView.as_view(), name="store"),
    path("responsaveis/", FocalListView.as_view(), name="focals"),
    path("rtvs/", RtvListView.as_view(), name="rtvs"),
]
