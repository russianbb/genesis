from django import forms

from .models import CompanyProduct


class CompanyProductForm(forms.ModelForm):
    class Meta:
        model = CompanyProduct
        fields = "__all__"
        exclude = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class": "form-control"}
