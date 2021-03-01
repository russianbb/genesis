from django.conf import settings  # TODO: remover no deploy
from django.conf.urls.static import static  # TODO: remover no deploy
from django.urls import path

from .views import (
    bill_create,
    bill_pay,
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
    path("despesas/cadastrar", expense_create, name="expense"),
    path("despesas/agendar", bill_create, name="bill"),
    path("despesas/<int:pk>/pagar", bill_pay, name="bill_pay"),
    path("recebiveis/", receivable_list, name="receivable_list"),
    path("recebiveis/adicionar", receivable_create, name="receivable"),
    path(
        "recebiveis/<int:number>/receber", receivable_receive, name="receivable_receive"
    ),
    path("dividendos/<int:number>/pagar", dividends_pay, name="dividend_pay"),
    path("extrato/", statement_report, name="statement_report"),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # TODO: remover no deploy
