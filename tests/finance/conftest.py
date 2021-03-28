from datetime import date, datetime
from decimal import Decimal

import pytest
from factories import (
    CostCenterFactory,
    InvoiceFactory,
    ServiceOrderFactory,
    TransactionCategoryFactory,
    TransactionFactory,
)


@pytest.fixture
def service_order():
    return ServiceOrderFactory(description="Some Service order")


@pytest.fixture
def cost_center():
    return CostCenterFactory(description="Some Cost Center")


@pytest.fixture
def cost_center_inactive():
    return CostCenterFactory(description="Some Inactive Cost Center", status=False)


@pytest.fixture
def invoice_not_received(service_order, cost_center):
    return InvoiceFactory(
        number=1,
        amount=Decimal(11.11),
        category="invoice",
        issued_at=datetime(2021, 1, 1),
        cost_center=cost_center,
        service_order=service_order,
        is_received=False,
    )


@pytest.fixture
def invoice_received(service_order, cost_center):
    return InvoiceFactory(
        number=2,
        amount=Decimal(22.22),
        category="invoice",
        issued_at=datetime(2021, 1, 1),
        cost_center=cost_center,
        service_order=service_order,
        is_received=True,
    )


@pytest.fixture
def invoice_last_year(service_order, cost_center):
    return InvoiceFactory(
        number=0,
        amount=Decimal(100.00),
        category="invoice",
        issued_at=datetime(2020, 1, 1),
        cost_center=cost_center,
        service_order=service_order,
        is_received=True,
    )


@pytest.fixture
def debit_received(service_order, cost_center):
    return InvoiceFactory(
        number=3,
        amount=Decimal(33.33),
        category="debit",
        issued_at=datetime(2021, 1, 1),
        cost_center=cost_center,
        service_order=service_order,
        is_received=True,
    )


@pytest.fixture
def debit_not_received(service_order, cost_center):
    return InvoiceFactory(
        number=4,
        amount=Decimal(44.00),
        category="debit",
        issued_at=datetime(2021, 1, 1),
        cost_center=cost_center,
        service_order=service_order,
        is_received=False,
    )


@pytest.fixture
def transaction_category():
    return TransactionCategoryFactory()


@pytest.fixture
def transaction_category_revenue():
    return TransactionCategoryFactory(
        description="Some fake revenue category", cash_flow="revenue"
    )


@pytest.fixture
def transaction(transaction_category, cost_center):
    return TransactionFactory(
        amount=Decimal(1.99), category=transaction_category, cost_center=cost_center
    )


@pytest.fixture
def transaction_not_paid(transaction_category, cost_center):
    return TransactionFactory(
        amount=Decimal(1.99),
        category=transaction_category,
        is_paid=False,
        due_date=date(2021, 1, 1),
        cost_center=cost_center,
    )


@pytest.fixture
def transaction_paid(transaction_category, cost_center):
    return TransactionFactory(
        amount=Decimal(1.99),
        category=transaction_category,
        transacted_at=date(2021, 1, 1),
        is_paid=True,
        notes="Some Notes",
        cost_center=cost_center,
    )


@pytest.fixture
def transaction_paid_with_due_date(transaction_category, cost_center):
    return TransactionFactory(
        amount=Decimal(1.99),
        category=transaction_category,
        due_date=date(2021, 1, 1),
        transacted_at=date(2021, 1, 1),
        is_paid=True,
        cost_center=cost_center,
    )


@pytest.fixture
def revenue_paid(transaction_category_revenue, cost_center):
    return TransactionFactory(
        amount=Decimal(10.00),
        category=transaction_category_revenue,
        transacted_at=date(2021, 1, 1),
        is_paid=True,
        cost_center=cost_center,
    )
