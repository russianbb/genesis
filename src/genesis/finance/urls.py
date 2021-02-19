from django.urls import path

from .views import expense_create

app_name = "finance"

urlpatterns = [
    path("despesa/", expense_create, name="expense"),
]
