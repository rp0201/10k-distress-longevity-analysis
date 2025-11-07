def get_liquidity_ratios(facts: dict) -> dict:
    return {
        'current_ratio': facts['current_assets'] / facts['current_liabilities'],
        'quick_ratio': (facts['current_assets'] - facts['inventory']) / facts['current_liabilities'],
    }

def get_leverage_ratios(facts: dict) -> dict:
    return {
        'debt_to_equity': facts['total_liabilities'] / facts['stockholders_equity'],
        'interest_coverage_ratio': (facts['revenue'] - facts['cost_of_goods_sold'] - facts['operating_expenses']) / facts['interest_expense']
    }

def get_profitability_ratios(facts: dict) -> dict:
    return {
        'ROA': facts['net_income'] / facts['total_assets'] * 100,
        'net_profit_margin': facts['net_income'] / facts['revenue']
    }

def get_cash_flow_ratios(facts: dict) -> dict:
    return {
        'operating_cash_flow': facts['operating_cash_flow'] / facts['current_liabilities'],
        'free_cash_flow_to_assets': (facts['operating_cash_flow'] - facts['capital_expenditure']) / facts['total_assets']
    }