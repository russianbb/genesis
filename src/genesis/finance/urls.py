from django.urls import path

from .views import (
    dividends_pay,
    expense_create,
    invoice_create,
    invoice_list,
    invoice_pay,
    statement_report,
)

app_name = "finance"

urlpatterns = [
    path("despesa/", expense_create, name="expense"),
    path("recebiveis/", invoice_list, name="invoice_list"),
    path("recebiveis/adicionar", invoice_create, name="invoice"),
    path("recebiveis/<int:number>/receber", invoice_pay, name="invoice_pay"),
    path("dividendos/<int:number>/pagar", dividends_pay, name="dividend_pay"),
    path("extrato/<str:start>/-/<str:end>", statement_report, name="statement_report"),
]
