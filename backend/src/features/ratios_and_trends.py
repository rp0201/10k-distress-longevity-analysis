def get_liquidity_ratios(facts: dict) -> dict:
    """
    Calculate liquidity ratios
    """
    return {
        'current_ratio': facts.get('current_assets') / facts.get('current_liabilities'),
        'quick_ratio': (facts.get('current_assets') - facts.get('inventory')) / facts.get('current_liabilities'),
    }

def get_leverage_ratios(facts: dict) -> dict:
    """
    Calculate leverage ratios
    """    
    interest_coverage = 0.0
    
    if facts.get('interest_expense') and facts.get('interest_expense') != 0:
        if facts.get('operating_income'):
            interest_coverage = facts.get('operating_income') / facts.get('interest_expense')
        else:
            # Fallback
            revenue = facts.get('revenue_current', 0)
            cogs = facts.get('cost_of_goods_sold', 0)
            opex = facts.get('operating_expenses', 0)
            
            if revenue:
                # Service/utility companies: Revenue - Operating Expenses
                # Product companies: Revenue - COGS - Operating Expenses
                operating_income = revenue - cogs - opex
                interest_coverage = operating_income / facts.get('interest_expense')
    
    return {
        'debt_to_equity': facts.get('total_liabilities') / facts.get('stockholders_equity'),
        'interest_coverage_ratio': interest_coverage
    }

def get_profitability_ratios(facts: dict) -> dict:
    """
    Calculate profitability ratios
    """
    return {
        'ROA': facts.get('net_income_current') / facts.get('total_assets') * 100,
        'net_profit_margin': facts.get('net_income_current') / facts.get('revenue_current')
    }

def get_cash_flow_ratios(facts: dict) -> dict:
    """
    Calculate cash flow ratios
    """
    return {
        'operating_cash_flow': facts.get('operating_cash_flow') / facts.get('current_liabilities'),
        'free_cash_flow_to_assets': (facts.get('operating_cash_flow') - facts.get('capital_expenditure')) / facts.get('total_assets')
    }

def get_revenue_pct_change(facts: dict) -> float:
    """
    Calculate revenue percent change
    """
    if facts.get('revenue_last') is None or facts.get('revenue_last') == 0:
        return 0.0
    return ((facts.get('revenue_current') - facts.get('revenue_last')) / abs(facts.get('revenue_last')))*100

def get_net_income_pct_change(facts: dict) -> float:
    """
    Calculate net income percent change
    """
    if facts.get('net_income_last') is None or facts.get('net_income_last') == 0:
        return 0.0
    return ((facts.get('net_income_current') - facts.get('net_income_last')) / abs(facts.get('net_income_last')))*100