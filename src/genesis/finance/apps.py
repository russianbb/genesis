from django.apps import AppConfig


class FinanceConfig(AppConfig):
    name = "finance"
    verbose_name = "Financeiro"

    def ready(self):
        import finance.signals  # noqa
