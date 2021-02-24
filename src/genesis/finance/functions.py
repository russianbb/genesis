from django.db.models import Sum

from .models import Transaction


def get_balance_until(date):
    get_receipt = Transaction.objects.filter(
        transacted_at__lt=date, category__cash_flow="receipt"
    ).aggregate(Sum("amount"))
    get_expense = Transaction.objects.filter(
        transacted_at__lt=date, category__cash_flow="expense"
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
            "document": _.document,
            "notes": _.notes,
        }
        reports.append(row)
    return reports
