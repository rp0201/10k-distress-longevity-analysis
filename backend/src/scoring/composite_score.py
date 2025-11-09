from src.features.ratios_and_trends import *
from src.models.bankruptcy_score import *
from src.scoring.interpreter import interpret_score

def normalize_ohlson(o_score: float) -> float:
    """
    Normalize Ohlson O-Score to 0-100 scale where lower is better.
    O-Score < -2: Very low risk (0-10)
    O-Score -2 to 0.5: Low to moderate risk (10-50)
    O-Score > 0.5: High risk (50-100)
    """
    if o_score < -2:
        return max(0, 10 + (o_score + 2) * 5)  # Cap at 0
    elif o_score <= 0.5:
        return 10 + (o_score + 2) * 16  # Scale from 10 to 50
    else:
        return min(100, 50 + (o_score - 0.5) * 25)  # Cap at 100

def normalize_growth(pct_change: float) -> float:
    """
    Normalize growth percentage to 0-100 where lower is better.
    Adjusted to be less harsh on mature companies with modest growth.
    < -20%: 80-100 (severe decline)
    -20% to -10%: 65-80 (bad)
    -10% to 0%: 40-65 (concerning to weak)
    0% to 5%: 20-40 (adequate for mature companies)
    5% to 15%: 5-20 (good growth)
    > 15%: 0-10 (excellent)
    """
    if pct_change < -20:
        return min(100, 80 + abs(pct_change + 20))
    elif pct_change < -10:
        return 65 + abs(pct_change + 10) * 1.5
    elif pct_change < 0:
        return 40 + abs(pct_change) * 2.5
    elif pct_change <= 5:
        return 20 + (5 - pct_change) * 4
    elif pct_change <= 15:
        return 5 + (15 - pct_change)
    else:
        return max(0, 5 - (pct_change - 15) * 0.33)

def normalize_liquidity(ratio: float, ideal: float = 2.0, has_strong_cf: bool = False) -> float:
    """
    Normalize liquidity ratios. Ideal is ~2.0.
    Too low (<1) is risky, too high (>3) suggests inefficiency.
    
    has_strong_cf: If True, reduces penalty for low working capital
                   (for companies with excellent cash generation)
    """
    if ratio < 1:
        base_score = 70 + (1 - ratio) * 30  # < 1 is bad (70-100)
        # Reduce penalty for companies with strong cash flow
        if has_strong_cf:
            return base_score * 0.6  # 40% discount on penalty
        return base_score
    elif ratio <= ideal:
        return 30 + (ideal - ratio) * 40  # 1-2 is good (30-70)
    elif ratio <= 3:
        return 30 + (ratio - ideal) * 20  # 2-3 is okay (30-50)
    else:
        return min(60, 50 + (ratio - 3) * 10)  # >3 slightly inefficient

def normalize_leverage(debt_to_equity: float) -> float:
    """
    Normalize debt-to-equity. Lower is better.
    < 0.5: Excellent (0-20)
    0.5-1.5: Good (20-40)
    1.5-3: Moderate (40-60)
    3-5: High (60-80)
    > 5: Very high (80-100)
    """
    if debt_to_equity < 0.5:
        return debt_to_equity * 40
    elif debt_to_equity <= 1.5:
        return 20 + (debt_to_equity - 0.5) * 20
    elif debt_to_equity <= 3:
        return 40 + (debt_to_equity - 1.5) * 13.33
    elif debt_to_equity <= 5:
        return 60 + (debt_to_equity - 3) * 10
    else:
        return min(100, 80 + (debt_to_equity - 5) * 4)

def normalize_interest_coverage(ratio: float) -> float:
    """
    Normalize interest coverage. Higher is better.
    
    Special handling:
    - Negative values or very high (>50) = treat as excellent 
      (either minimal debt or data quality issue with EBIT calculation)
    < 1: Very risky (80-100)
    1-2.5: Risky (60-80)
    2.5-5: Moderate (40-60)
    5-10: Good (20-40)
    > 10: Excellent (0-20)
    """
    # Handle edge cases: negative EBIT or extremely high coverage
    if ratio < 0 or ratio > 50:
        return 0  # Treat as no debt concerns
    elif ratio < 1:
        return 80 + (1 - ratio) * 20
    elif ratio <= 2.5:
        return 60 + (2.5 - ratio) * 13.33
    elif ratio <= 5:
        return 40 + (5 - ratio) * 8
    elif ratio <= 10:
        return 20 + (10 - ratio) * 4
    else:
        return max(0, 20 - (ratio - 10) * 2)

def normalize_profitability(roa: float) -> float:
    """
    Normalize ROA percentage. Higher is better.
    < 0: Very bad (80-100)
    0-5: Poor (60-80)
    5-10: Fair (40-60)
    10-20: Good (20-40)
    > 20: Excellent (0-20)
    """
    if roa < 0:
        return min(100, 80 + abs(roa) * 2)
    elif roa <= 5:
        return 60 + (5 - roa) * 4
    elif roa <= 10:
        return 40 + (10 - roa) * 4
    elif roa <= 20:
        return 20 + (20 - roa) * 2
    else:
        return max(0, 20 - (roa - 20) * 0.5)

def normalize_cash_flow(ratio: float, threshold: float = 0.5) -> float:
    """
    Normalize cash flow ratios. Higher is better.
    < 0: Very bad (80-100)
    0-threshold: Poor (60-80)
    threshold-1: Good (30-60)
    > 1: Excellent (0-30)
    """
    if ratio < 0:
        return min(100, 80 + abs(ratio) * 20)
    elif ratio <= threshold:
        return 60 + (threshold - ratio) / threshold * 40
    elif ratio <= 1:
        return 30 + (1 - ratio) / (1 - threshold) * 30
    else:
        return max(0, 30 - (ratio - 1) * 15)

def calculate_composite(facts: dict) -> dict:
    """
    Calculate composite distress score (0-100 scale).
    Lower score = Better (healthier company)
    
    Returns dict with:
    - score: float (0-100)
    - grade: str (A-F)
    - risk_level: str
    - interpretation: str
    - components: dict of individual scores
    """
    cf_ratios = get_cash_flow_ratios(facts)
    leverage_ratios = get_leverage_ratios(facts)
    liquidity_ratios = get_liquidity_ratios(facts)
    profitability_ratios = get_profitability_ratios(facts)
    
    revenue_pct = get_revenue_pct_change(facts)
    net_income_pct = get_net_income_pct_change(facts)
    ohlson_score = get_ohlson_oscore(facts)
    
    # Check if company has strong cash flow (for liquidity adjustment)
    has_strong_cf = cf_ratios['operating_cash_flow'] > 0.4
    
    # Normalize all components (0-100, lower is better)
    o_norm = normalize_ohlson(ohlson_score)
    revenue_norm = normalize_growth(revenue_pct)
    ni_norm = normalize_growth(net_income_pct)
    current_ratio_norm = normalize_liquidity(
        liquidity_ratios['current_ratio'], 
        ideal=2.0, 
        has_strong_cf=has_strong_cf
    )
    quick_ratio_norm = normalize_liquidity(
        liquidity_ratios['quick_ratio'], 
        ideal=1.5, 
        has_strong_cf=has_strong_cf
    )
    dte_norm = normalize_leverage(leverage_ratios['debt_to_equity'])
    int_cov_norm = normalize_interest_coverage(leverage_ratios['interest_coverage_ratio'])
    roa_norm = normalize_profitability(profitability_ratios['ROA'])
    npm_norm = normalize_profitability(profitability_ratios['net_profit_margin'] * 100)
    ocf_norm = normalize_cash_flow(cf_ratios['operating_cash_flow'], threshold=0.15)
    fcf_norm = normalize_cash_flow(cf_ratios['free_cash_flow_to_assets'], threshold=0.05)
    
    # Store component scores for transparency
    components = {
        'ohlson': {'score': o_norm, 'weight': 0.10, 'raw': ohlson_score},
        'revenue_growth': {'score': revenue_norm, 'weight': 0.15, 'raw': revenue_pct},
        'net_income_growth': {'score': ni_norm, 'weight': 0.15, 'raw': net_income_pct},
        'operating_cf': {'score': ocf_norm, 'weight': 0.12, 'raw': cf_ratios['operating_cash_flow']},
        'free_cf': {'score': fcf_norm, 'weight': 0.08, 'raw': cf_ratios['free_cash_flow_to_assets']},
        'current_ratio': {'score': current_ratio_norm, 'weight': 0.08, 'raw': liquidity_ratios['current_ratio']},
        'quick_ratio': {'score': quick_ratio_norm, 'weight': 0.07, 'raw': liquidity_ratios['quick_ratio']},
        'debt_to_equity': {'score': dte_norm, 'weight': 0.08, 'raw': leverage_ratios['debt_to_equity']},
        'interest_coverage': {'score': int_cov_norm, 'weight': 0.07, 'raw': leverage_ratios['interest_coverage_ratio']},
        'roa': {'score': roa_norm, 'weight': 0.05, 'raw': profitability_ratios['ROA']},
        'net_margin': {'score': npm_norm, 'weight': 0.05, 'raw': profitability_ratios['net_profit_margin']}
    }
    
    # Weighted composite (weights sum to 1.0)
    composite = (
        o_norm * 0.10 +              # Ohlson O-Score (bankruptcy risk) - 10%
        revenue_norm * 0.15 +         # Revenue growth - 15%
        ni_norm * 0.15 +              # Net income growth - 15%
        ocf_norm * 0.12 +             # Operating cash flow - 12%
        fcf_norm * 0.08 +             # Free cash flow - 8%
        current_ratio_norm * 0.08 +   # Current ratio - 8%
        quick_ratio_norm * 0.07 +     # Quick ratio - 7%
        dte_norm * 0.08 +             # Debt-to-equity - 8%
        int_cov_norm * 0.07 +         # Interest coverage - 7%
        roa_norm * 0.05 +             # ROA - 5%
        npm_norm * 0.05               # Net profit margin - 5%
    )
    
    # Get interpretation from interpreter module
    interpretation_data = interpret_score(composite)
    
    return {
        'score': round(composite, 2),
        'grade': interpretation_data['grade'],
        'risk_level': interpretation_data['risk_level'],
        'interpretation': interpretation_data['interpretation'],
        'components': components
    }