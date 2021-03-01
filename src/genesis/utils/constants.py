TRANSACTION_CATEGORY_DIVIDENDS = {"cash_flow": "expense", "description": "Dividendos"}
TRANSACTION_CATEGORY_LOAN_OUT = {
    "cash_flow": "expense",
    "description": "Empréstimo Pagamento",
}
TRANSACTION_CATEGORY_LOAN_IN = {
    "cash_flow": "revenue",
    "description": "Empréstimo Recebimento",
}
TRANSACTION_CATEGORY_NF = {"cash_flow": "revenue", "description": "Nota Fiscal"}
TRANSACTION_CATEGORY_ND = {"cash_flow": "revenue", "description": "Nota de Débito"}

BASE_TRANSACTION_CATEGORIES = (
    TRANSACTION_CATEGORY_DIVIDENDS,
    TRANSACTION_CATEGORY_NF,
    TRANSACTION_CATEGORY_ND,
    TRANSACTION_CATEGORY_LOAN_IN,
    TRANSACTION_CATEGORY_LOAN_OUT,
)


COSTCENTER_ADMINISTRATIVE = {"description": "Administrativo"}
BASE_COSTCENTER = (COSTCENTER_ADMINISTRATIVE,)
