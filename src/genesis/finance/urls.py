from django.urls import path

from .views import (
    dashboard,
    dividends_pay,
    expense_create,
    invoice_create,
    invoice_list,
    invoice_pay,
    statement_report,
)

app_name = "finance"

urlpatterns = [
    path("painel/", dashboard, name="dashboard"),
    path("despesa/", expense_create, name="expense"),
    path("recebiveis/", invoice_list, name="invoice_list"),
    path("recebiveis/adicionar", invoice_create, name="invoice"),
    path("recebiveis/<int:number>/receber", invoice_pay, name="invoice_pay"),
    path("dividendos/<int:number>/pagar", dividends_pay, name="dividend_pay"),
    path("extrato/", statement_report, name="statement_report"),
]
