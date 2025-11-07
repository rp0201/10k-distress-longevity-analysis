import math

def get_altman_zscore(facts: dict) -> float:
    '''
    Z' = 0.717*X1 + 0.847*X2 + 3.107*X3 + 0.420*X4 + 0.998*X5

    X1 = Working Capital / Total Assets
    X2 = Retained Earnings / Total Assets
    X3 = EBIT / Total Assets -- EBIT = Revenue – Cost of goods sold – Operating Expenses
    X4 = Book Value of Equity / Total Liabilities
    X5 = Sales / Total Assets 

    Interpretation:
    **Z' > 2.9** = Safe Zone
    **1.23 < Z' < 2.9** = Gray Zone
    **Z' < 1.23** = Distress Zone
    '''
    
    ta = facts['total_assets']
    tl = facts['total_liabilities']
    wc = facts['current_assets'] - facts['current_liabilities']
    x1 = wc / ta
    x2 = facts['retained_earnings'] / ta
    x3 = (facts['revenue'] - facts['cost_of_goods_sold'] - facts['operating_expenses']) / ta
    book_value_equity = facts['total_assets'] - facts['total_liabilities']
    x4 = book_value_equity / tl if tl != 0 else 0
    x5 = facts['revenue'] / ta
    
    z_score = 0.717*x1 + 0.847*x2 + 3.107*x3 + 0.420*x4 + 0.998*x5
    
    return z_score

def get_ohlson_oscore(facts: dict) -> float:
    '''
    O = -1.32 - 0.407*log(TA) + 6.03*(TL/TA) - 1.43*(WC/TA) + 0.0757*(CL/CA) - 2.37*(NI/TA) - 1.83*(FFO/TL) + 0.285*INTWO - 1.72*OENEG - 0.521*CHIN

    TA = Total Assets (in thousands)
    TL = Total Liabilities
    WC = Working Capital (Current Assets - Current Liabilities)
    CA = Current Assets
    CL = Current Liabilities
    NI = Net Income
    FFO = Funds From Operations (approximated as Net Income + Depreciation)
    INTWO = 1 if Net Income was negative for last 2 years, else 0
    OENEG = 1 if Total Liabilities > Total Assets, else 0
    CHIN = (NI_t - NI_(t-1)) / (|NI_t| + |NI_(t-1)|)

    Interpretation:
    O > 0.5 = High probability of bankruptcy (>50%)
    O < 0.5 = Low probability of bankruptcy
    '''

    ta = facts['total_assets']
    tl = facts['total_liabilities']
    wc = facts['current_assets'] - facts['current_liabilities']
    ca = facts['current_assets']
    cl = facts['current_liabilities']
    nic = facts['net_income_current']
    nil = facts['net_income_last']
    ffo = facts['net_income_current'] + facts['depreciation']
    intwo = 1 if nic < 0 and nil < 0 else 0
    oeneg = 1 if tl > ta else 0
    chin = 0 if (abs(nic) + abs(nil) == 0) else ((nic - nil) / (abs(nic) + abs(nil)))

    o_score = -1.32 - 0.407*math.log(ta / 1000) + 6.03*(tl/ta) - 1.43*(wc/ta) + 0.0757*(cl/ca) - 2.37*(nic/ta) - 1.83*(ffo/tl) + 0.285*intwo - 1.72*oeneg - 0.521*chin

    return o_score