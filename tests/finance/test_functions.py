from datetime import date
from decimal import Decimal

import pytest
from finance.functions import (
    get_active_cost_center,
    get_balance_until,
    get_billings_history,
    get_bills_not_paid,
    get_dividends_receiver_choices,
    get_receivables_not_received_data,
    process_statement_report,
)
from finance.models import CostCenter
from freezegun import freeze_time

pytestmark = pytest.mark.django_db


def test_get_bills_not_paid(transaction_paid, transaction_not_paid):
    response = get_bills_not_paid()

    assert len(response) == 1
    assert response[0].id == transaction_not_paid.id


def test_get_active_cost_center(cost_center, cost_center_inactive):
    # Administrativo auto created with finance.app
    assert len(CostCenter.objects.all()) == 3
    response = get_active_cost_center()

    assert len(response) == 1
    assert response[0].id == cost_center.id


def test_get_receivables_not_received_data(
    debit_not_received, invoice_not_received, invoice_received
):
    response = get_receivables_not_received_data()

    amount = debit_not_received.amount + invoice_not_received.amount

    assert type(response) is dict
    assert len(response["receivables_not_received"]) == 2
    assert "amount_not_received" in response.keys()
    assert "receivables_not_received" in response.keys()
    assert float(response["amount_not_received"]) == float(amount)

    not_received = response["receivables_not_received"]
    assert not_received[0].id == debit_not_received.id
    assert not_received[1].id == invoice_not_received.id


@freeze_time("2021-01-02")
def test_get_billings_history(
    invoice_not_received, invoice_received, invoice_last_year
):
    response = get_billings_history()

    assert type(response) is dict
    assert "billings_12_months" in response.keys()
    assert "billings_annual" in response.keys()

    assert float(response["billings_12_months"]) == invoice_last_year.amount

    annual_sum = invoice_not_received.amount + invoice_received.amount
    assert float(response["billings_annual"]) == float(annual_sum)


def test_get_balance_until(revenue_paid, transaction_paid):
    response = get_balance_until(date=date(2021, 1, 1))

    expected_balance = revenue_paid.amount - transaction_paid.amount
    assert float(response) == float(expected_balance)


def test_get_dividends_receiver_choices(super_user, user):
    response = get_dividends_receiver_choices()
    assert len(response) == 1
    assert response[0] == (super_user.username, super_user.get_full_name)


def test_process_statement_report(transaction_paid, transaction_paid_with_due_date):
    context = {}
    context["start_balance"] = Decimal(0.00)
    context["transactions"] = [transaction_paid, transaction_paid_with_due_date]

    response = process_statement_report(context)
    assert len(response) == 2

    balance = context["start_balance"] - transaction_paid.amount
    assert response[0]["transacted_at"] == transaction_paid.transacted_at
    assert response[0]["category"] == transaction_paid.category
    assert float(response[0]["amount"]) == -float(transaction_paid.amount)
    assert response[0]["notes"] == transaction_paid.notes
    assert response[0]["balance"] == balance

    balance = balance - transaction_paid_with_due_date.amount
    assert response[1]["transacted_at"] == transaction_paid_with_due_date.transacted_at
    assert response[1]["category"] == transaction_paid_with_due_date.category
    assert float(response[0]["amount"]) == -float(transaction_paid_with_due_date.amount)
    assert response[1]["notes"] == transaction_paid_with_due_date.notes
    assert response[1]["balance"] == balance
