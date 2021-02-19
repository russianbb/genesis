from django import forms

from .models import Category, Transaction


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
        self.fields["category"].queryset = Category.objects.filter(cash_flow="expense")
