from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Sum

from .models import CostCenter, Receivable, Transaction


def get_cost_center_chart_data():
    pass


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
    get_receipt = Transaction.objects.filter(
        transacted_at__lte=date, category__cash_flow="receipt"
    ).aggregate(Sum("amount"))
    get_expense = Transaction.objects.filter(
        transacted_at__lte=date, category__cash_flow="expense"
    ).aggregate(Sum("amount"))
    receipt = 0 if get_receipt["amount__sum"] is None else get_receipt["amount__sum"]
    expense = 0 if get_expense["amount__sum"] is None else get_expense["amount__sum"]
    balance = receipt - expense
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
