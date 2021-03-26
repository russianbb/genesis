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
def invoice_not_received(service_order, cost_center):
    return InvoiceFactory(
        number=1,
        amount=11.11,
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
        amount=22.22,
        category="invoice",
        issued_at=datetime(2021, 1, 1),
        cost_center=cost_center,
        service_order=service_order,
        is_received=True,
    )


@pytest.fixture
def debit_received(service_order, cost_center):
    return InvoiceFactory(
        number=3,
        amount=33.33,
        category="debit",
        issued_at=datetime(2021, 1, 1),
        cost_center=cost_center,
        service_order=service_order,
        is_received=True,
    )


@pytest.fixture
def transaction_category():
    return TransactionCategoryFactory()


@pytest.fixture
def transaction(transaction_category):
    return TransactionFactory(amount=Decimal(1.99), category=transaction_category,)


@pytest.fixture
def transaction_not_paid(transaction_category):
    return TransactionFactory(
        amount=Decimal(1.99),
        category=transaction_category,
        is_paid=False,
        due_date=date(2021, 1, 1),
    )


@pytest.fixture
def transaction_paid(transaction_category):
    return TransactionFactory(
        amount=Decimal(1.99),
        category=transaction_category,
        transacted_at=date(2021, 1, 1),
        is_paid=True,
        notes="Some Notes",
    )


@pytest.fixture
def transaction_paid_with_due_date(transaction_category):
    return TransactionFactory(
        amount=Decimal(1.99),
        category=transaction_category,
        due_date=date(2021, 1, 1),
        transacted_at=date(2021, 1, 1),
        is_paid=True,
    )
