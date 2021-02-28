from django.apps import AppConfig
from django.db.models.signals import post_migrate
from utils.constants import (
    PREPOPULATED_FINANCE_CATEGORIES,
    PREPOPULATED_FINANCE_COSTCENTER,
)


class FinanceConfig(AppConfig):
    name = "finance"
    verbose_name = "Financeiro"

    def ready(self):
        post_migrate.connect(prepopulate_categories, sender=self)
        post_migrate.connect(prepopulate_cost_center, sender=self)
        import finance.signals  # noqa


def prepopulate_categories(sender, **kwargs):
    from .models import Category

    for _ in PREPOPULATED_FINANCE_CATEGORIES:
        cash_flow = _["cash_flow"]
        description = _["description"]
        Category.objects.get_or_create(cash_flow=cash_flow, description=description)


def prepopulate_cost_center(sender, **kwargs):
    from .models import CostCenter

    for _ in PREPOPULATED_FINANCE_COSTCENTER:
        description = _["description"]
        CostCenter.objects.get_or_create(description=description)
