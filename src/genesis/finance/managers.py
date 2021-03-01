from django.db import models


class BillManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_paid=False, category__cash_flow="expense")


class ExpenseManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_paid=True, category__cash_flow="expense")


class RevenueManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category__cash_flow="revenue")
