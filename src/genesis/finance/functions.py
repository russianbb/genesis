from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db.models import Sum

from .models import Bill, CostCenter, Expense, Receivable, Revenue


def get_cost_center_chart_data():
    pass  # TODO: como somar por grupo?


def get_bills_not_paid():
    return Bill.objects.all()


def get_active_cost_center():
    return (
        CostCenter.objects.filter(status=True)
        .exclude(description="Administrativo")
        .all()
    )


def get_receivables_not_received_data():
    amount_not_received = 0
    query = Receivable.objects.all()

    not_received = query.filter(is_received=False)

    aggregate_not_received = not_received.aggregate(Sum("amount"))
    if aggregate_not_received.get("amount__sum"):
        amount_not_received = aggregate_not_received["amount__sum"]

    return {
        "amount_not_received": amount_not_received,
        "receivables_not_received": not_received,
    }


def get_billings_history():
    billings_12_months = 0
    billings_annual = 0

    today = datetime.now()

    begin_12_months = (today - relativedelta(years=1)).replace(day=1)
    end_12_months = today.replace(day=1) - relativedelta(days=1)

    query = Receivable.objects.filter(category="invoice").all()

    aggregate_12_months = query.filter(
        issued_at__gte=begin_12_months, issued_at__lte=end_12_months
    ).aggregate(Sum("amount"))
    if aggregate_12_months.get("amount__sum"):
        billings_12_months = aggregate_12_months["amount__sum"]

    begin_year = today.replace(day=1, month=1)
    aggregate_annual = query.filter(
        issued_at__gte=begin_year, issued_at__lte=today
    ).aggregate(Sum("amount"))
    if aggregate_annual.get("amount__sum"):
        billings_annual = aggregate_annual["amount__sum"]

    return {
        "billings_12_months": billings_12_months,
        "billings_annual": billings_annual,
    }


def get_balance_until(date=datetime.now()):
    sum_revenue = Revenue.objects.filter(transacted_at__lte=date).aggregate(
        Sum("amount")
    )
    sum_expense = Expense.objects.filter(transacted_at__lte=date).aggregate(
        Sum("amount")
    )
    revenue = 0 if sum_revenue["amount__sum"] is None else sum_revenue["amount__sum"]
    expense = 0 if sum_expense["amount__sum"] is None else sum_expense["amount__sum"]
    balance = revenue - expense
    return balance


def process_statement_report(context):
    balance = context["start_balance"]
    reports = []
    for _ in context["transactions"]:
        amount = _.amount
        if _.category.cash_flow == "expense":
            amount = _.amount * -1
        balance += amount
        row = {
            "transacted_at": _.transacted_at,
            "category": _.category,
            "cost_center": _.cost_center,
            "amount": amount,
            "balance": balance,
            "file": _.file,
            "notes": _.notes,
        }
        reports.append(row)
    return reports


def get_dividends_receiver_choices():
    superusers = User.objects.filter(is_superuser=True).all()
    receiver_choices = []
    for _ in superusers:
        receiver_choices.append((_.username, _.get_full_name))
    return receiver_choices
