from unittest.mock import Mock, patch

import pytest
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from finance.admin import (
    BillAdmin,
    CostCenterAdmin,
    DividendsInline,
    ExpenseAdmin,
    PaidInline,
    ReceivableAdmin,
    ReceivableInline,
    RevenueAdmin,
    ServiceOrderAdmin,
    TransactionAdmin,
    TransactionCategoryAdmin,
)
from finance.models import (
    Bill,
    CostCenter,
    Expense,
    Receivable,
    Revenue,
    ServiceOrder,
    Transaction,
    TransactionCategory,
)
from rangefilter.filter import DateRangeFilter
from utils.admin import ReadOnlyAdminMixin
from utils.constants import TRANSACTION_CATEGORY_DIVIDENDS

pytestmark = pytest.mark.django_db


class TestReceivableInlineAdmin:
    def setup_method(self):
        self.admin = ReceivableInline(Receivable, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, ReadOnlyAdminMixin)
        assert isinstance(self.admin, admin.TabularInline)

    def test_admin_attributes(self):
        assert self.admin.model == Receivable
        assert self.admin.fields == (
            "get_amount_display",
            "category",
            "issued_at",
            "is_received",
        )
        assert self.admin.readonly_fields == self.admin.fields
        assert self.admin.extra == 0

    def test_get_amount_display(self, invoice_received):
        assert self.admin.get_amount_display(invoice_received) == "22,22"
        assert self.admin.get_amount_display.short_description == "Valor"


class TestPaidInlineAdmin:
    def setup_method(self):
        self.admin = PaidInline(Revenue, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, ReadOnlyAdminMixin)
        assert isinstance(self.admin, admin.TabularInline)

    def test_admin_attributes(self):
        assert self.admin.model == Revenue
        assert self.admin.fields == ("get_amount_display", "category", "transacted_at")
        assert self.admin.readonly_fields == self.admin.fields
        assert self.admin.extra == 0
        assert self.admin.verbose_name == "Recebido"
        assert self.admin.verbose_name_plural == "Recebidos"

    def test_get_amount_display(self, invoice_received):
        assert self.admin.get_amount_display(invoice_received) == "22,22"
        assert self.admin.get_amount_display.short_description == "Valor"


class TestDividendsInlineAdmin:
    def setup_method(self):
        self.admin = DividendsInline(Transaction, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, ReadOnlyAdminMixin)
        assert isinstance(self.admin, admin.TabularInline)

    def test_admin_attributes(self):
        assert self.admin.model == Transaction
        assert self.admin.fields == ("get_amount_display", "category", "transacted_at")
        assert self.admin.readonly_fields == self.admin.fields
        assert self.admin.extra == 0
        assert self.admin.verbose_name == "Dividendos Pagos"
        assert self.admin.verbose_name_plural == "Dividendos Pagos"

    def test_get_amount_display(self, transaction):
        assert self.admin.get_amount_display(transaction) == "1,99"
        assert self.admin.get_amount_display.short_description == "Valor"

    @patch("finance.admin.super")
    def test_get_queryset(self, mock_super):
        request = Mock()
        self.admin.get_queryset(request)

        mock_super.return_value.get_queryset.assert_called_once_with(request)

        queryset = mock_super.return_value.get_queryset.return_value
        queryset.filter.assert_called_once_with(
            category__cash_flow=TRANSACTION_CATEGORY_DIVIDENDS["cash_flow"],
            category__description=TRANSACTION_CATEGORY_DIVIDENDS["description"],
        )


class TestReceivableAdmin:
    def setup_method(self):
        self.admin = ReceivableAdmin(Receivable, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, admin.ModelAdmin)

    def test_admin_attributes(self):
        assert self.admin.list_display == (
            "get_number_display",
            "category",
            "get_amount_display",
            "cost_center",
            "service_order",
            "issued_at",
            "is_received",
        )
        assert self.admin.list_display_links == self.admin.list_display
        assert self.admin.search_fields == self.admin.list_display
        assert self.admin.list_filter == (
            "category",
            ("issued_at", DateRangeFilter),
            "service_order",
        )

    def test_get_amount_display(self, invoice_not_received):
        assert self.admin.get_amount_display(invoice_not_received) == "11,11"
        assert self.admin.get_amount_display.short_description == "Valor"

    def test_get_number_display(self, invoice_not_received):
        assert self.admin.get_number_display(invoice_not_received) == "001"
        assert self.admin.get_number_display.short_description == "Número"


class TestCostCenterAdmin:
    def setup_method(self):
        self.admin = CostCenterAdmin(CostCenter, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, admin.ModelAdmin)

    def test_admin_attributes(self):
        assert self.admin.list_display == ("id", "description", "updated_at", "status")
        assert self.admin.list_display_links == ("id", "description")
        assert self.admin.search_fields == ("id", "description")
        assert self.admin.list_filter == ("status",)
        assert self.admin.inlines == (ReceivableInline, PaidInline, DividendsInline)


class TestTransactionCategoryAdmin:
    def setup_method(self):
        self.admin = TransactionCategoryAdmin(TransactionCategory, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, admin.ModelAdmin)

    def test_admin_attributes(self):
        assert self.admin.list_display == (
            "id",
            "cash_flow",
            "description",
            "updated_at",
            "status",
        )
        assert self.admin.list_display_links == ("id", "cash_flow", "description")
        assert self.admin.search_fields == ("id", "description")
        assert self.admin.list_filter == ("cash_flow", "status")


class TestServiceOrderAdmin:
    def setup_method(self):
        self.admin = ServiceOrderAdmin(ServiceOrder, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, admin.ModelAdmin)

    def test_admin_attributes(self):
        assert self.admin.list_display == (
            "id",
            "description",
            "buy_order",
            "updated_at",
            "status",
        )
        assert self.admin.list_display_links == ("id", "description")
        assert self.admin.search_fields == ("id", "description", "buy_order", "status")
        assert self.admin.list_filter == ("status",)


class TestBillAdmin:
    def setup_method(self):
        self.admin = BillAdmin(Bill, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, admin.ModelAdmin)

    def test_admin_attributes(self):
        assert self.admin.list_display == (
            "id",
            "category",
            "cost_center",
            "get_amount_display",
            "due_date",
            "is_paid",
        )
        assert self.admin.list_display_links == self.admin.list_display
        assert self.admin.search_fields == (
            "id",
            "category__description",
            "cost_center__description",
            "notes",
            "amount",
        )
        assert self.admin.list_filter == (
            "category",
            "cost_center",
            ("due_date", DateRangeFilter),
        )

    def test_get_amount_display(self, transaction_paid):
        assert self.admin.get_amount_display(transaction_paid) == "1,99"
        assert self.admin.get_amount_display.short_description == "Valor"


class TestExpenseAdmin:
    def setup_method(self):
        self.admin = ExpenseAdmin(Expense, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, admin.ModelAdmin)

    def test_admin_attributes(self):
        assert self.admin.list_display == (
            "id",
            "category",
            "cost_center",
            "get_amount_display",
            "transacted_at",
            "is_paid",
        )
        assert self.admin.list_display_links == self.admin.list_display
        assert self.admin.search_fields == (
            "id",
            "category__description",
            "cost_center__description",
            "notes",
            "amount",
        )
        assert self.admin.list_filter == (
            "category",
            "cost_center",
            ("transacted_at", DateRangeFilter),
        )

    def test_get_amount_display(self, transaction_paid):
        assert self.admin.get_amount_display(transaction_paid) == "1,99"
        assert self.admin.get_amount_display.short_description == "Valor"


class TestRevenueAdmin:
    def setup_method(self):
        self.admin = RevenueAdmin(Revenue, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, admin.ModelAdmin)

    def test_admin_attributes(self):
        assert self.admin.list_display == (
            "id",
            "category",
            "cost_center",
            "get_amount_display",
            "transacted_at",
            "is_paid",
        )
        assert self.admin.list_display_links == self.admin.list_display
        assert self.admin.search_fields == (
            "id",
            "category__description",
            "cost_center__description",
            "notes",
            "amount",
        )
        assert self.admin.list_filter == (
            "category",
            "cost_center",
            ("transacted_at", DateRangeFilter),
        )

    def test_get_amount_display(self, transaction_paid):
        assert self.admin.get_amount_display(transaction_paid) == "1,99"
        assert self.admin.get_amount_display.short_description == "Valor"


class TestTransactionAdmin:
    def setup_method(self):
        self.admin = TransactionAdmin(Transaction, AdminSite())

    def test_admin_subclass(self):
        assert isinstance(self.admin, admin.ModelAdmin)

    def test_admin_attributes(self):
        assert self.admin.list_display == (
            "id",
            "category",
            "cost_center",
            "get_amount_display",
            "transacted_at",
            "due_date",
            "is_paid",
        )
        assert self.admin.list_display_links == self.admin.list_display
        assert self.admin.search_fields == (
            "id",
            "category__description",
            "cost_center__description",
            "notes",
            "amount",
        )
        assert self.admin.list_filter == (
            "cost_center",
            "is_paid",
            ("transacted_at", DateRangeFilter),
            "category",
        )

    def test_get_amount_display(self, transaction_paid):
        assert self.admin.get_amount_display(transaction_paid) == "1,99"
        assert self.admin.get_amount_display.short_description == "Valor"
