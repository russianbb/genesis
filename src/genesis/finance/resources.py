from import_export import resources
from import_export.fields import Field

from .models import Transaction


class TransactionResource(resources.ModelResource):
    id = Field(attribute="pk", column_name="Id")
    due_date = Field(attribute="due_date ", column_name="Data Vencimento")
    transacted_at = Field(attribute="transacted_at", column_name="Data Transação")
    amount = Field(attribute="get_amount_display", column_name="Valor")
    cost_center = Field(attribute="cost_center", column_name="Centro de Custo")
    category = Field(attribute="category", column_name="Categoria")
    cash_flow = Field(attribute="category__cash_flow", column_name="Fluxo")
    notes = Field(attribute="notes", column_name="Anotações")
    is_paid = Field(attribute="is_paid", column_name="Pago?")
    is_recurrent = Field(attribute="is_recurrent", column_name="Recorrente?")

    class Meta:
        model = Transaction
        fields = (
            "id",
            "due_date",
            "transacted_at",
            "cash_flow",
            "amount",
            "cost_center",
            "category",
            "notes",
            "is_paid",
            "is_recurrent",
        )
        export_order = fields

    def dehydrate_due_date(self, obj):
        if obj.due_date:
            return obj.due_date.strftime("%d/%m/%Y")
        return "-"

    def dehydrate_transacted_at(self, obj):
        if obj.transacted_at:
            return obj.transacted_at.strftime("%d/%m/%Y")
        return "-"

    def dehydrate_cash_flow(self, obj):
        obj.category.get_cash_flow_display()

    def dehydrate_is_paid(self, obj):
        return "Sim" if obj.is_paid else "Não"

    def dehydrate_is_recurrent(self, obj):
        return "Sim" if obj.is_paid else "Não"
