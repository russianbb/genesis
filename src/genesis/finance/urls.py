from django.urls import path

from .views import (
    dashboard,
    dividends_pay,
    expense_create,
    receivable_create,
    receivable_list,
    receivable_receive,
    statement_report,
)

app_name = "finance"

urlpatterns = [
    path("painel/", dashboard, name="dashboard"),
    path("despesas/", expense_create, name="expense"),
    path("recebiveis/", receivable_list, name="receivable_list"),
    path("recebiveis/adicionar", receivable_create, name="receivable"),
    path(
        "recebiveis/<int:number>/receber", receivable_receive, name="receivable_receive"
    ),
    path("dividendos/<int:number>/pagar", dividends_pay, name="dividend_pay"),
    path("extrato/", statement_report, name="statement_report"),
]
