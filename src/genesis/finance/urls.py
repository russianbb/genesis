from django.urls import path

from .views import (
    expense_create,
    invoice_create,
    invoice_detail,
    invoice_list,
    invoice_pay,
)

app_name = "finance"

urlpatterns = [
    path("despesa/", expense_create, name="expense"),
    path("recebiveis/", invoice_list, name="invoice_list"),
    path("recebiveis/adicionar", invoice_create, name="invoice"),
    path("recebiveis/<int:number>", invoice_detail, name="invoice_detail"),
    path("recebiveis/<int:number>/receber", invoice_pay, name="invoice_pay"),
]
