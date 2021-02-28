CATEGORY_DIVIDENDS = {"cash_flow": "expense", "description": "Pagamento de Dividendos"}
CATEGORY_LOAN_OUT = {"cash_flow": "expense", "description": "Pagamento de Empréstimo"}
CATEGORY_LOAN_IN = {"cash_flow": "revenue", "description": "Recebimento de Empréstimo"}
CATEGORY_NF = {"cash_flow": "revenue", "description": "Recebimento de Nota Fiscal"}
CATEGORY_ND = {"cash_flow": "revenue", "description": "Recebimento de Nota de Débito"}

PREPOPULATED_FINANCE_CATEGORIES = (
    CATEGORY_DIVIDENDS,
    CATEGORY_NF,
    CATEGORY_ND,
    CATEGORY_LOAN_IN,
    CATEGORY_LOAN_OUT,
)


COSTCENTER_ADMINISTRATIVE = {"description": "Administrativo"}
PREPOPULATED_FINANCE_COSTCENTER = (COSTCENTER_ADMINISTRATIVE,)
