from datetime import datetime

import pytest
from factories import (
    CostCenterFactory,
    InvoiceFactory,
    ServiceOrderFactory,
    TransactionCategoryFactory,
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
