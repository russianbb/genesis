from django.apps import AppConfig
from django.db.models.signals import post_migrate
from utils.constants import BASE_COSTCENTER, BASE_TRANSACTION_CATEGORIES


class FinanceConfig(AppConfig):
    name = "finance"
    verbose_name = "Financeiro"

    def ready(self):
        post_migrate.connect(prepopulate_categories, sender=self)
        post_migrate.connect(prepopulate_cost_center, sender=self)


def prepopulate_categories(sender, **kwargs):
    from .models import TransactionCategory

    for _ in BASE_TRANSACTION_CATEGORIES:
        cash_flow = _["cash_flow"]
        description = _["description"]
        TransactionCategory.objects.get_or_create(
            cash_flow=cash_flow, description=description
        )


def prepopulate_cost_center(sender, **kwargs):
    from .models import CostCenter

    for _ in BASE_COSTCENTER:
        description = _["description"]
        CostCenter.objects.get_or_create(description=description)
