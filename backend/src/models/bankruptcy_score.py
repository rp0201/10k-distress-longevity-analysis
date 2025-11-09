import math

def get_ohlson_oscore(facts: dict) -> float:
    """
    Calculates ohlson bankruptcy score
    """

    ta = facts.get('total_assets')
    tl = facts.get('total_liabilities')
    wc = facts.get('current_assets') - facts.get('current_liabilities')
    ca = facts.get('current_assets')
    cl = facts.get('current_liabilities')
    nic = facts.get('net_income_current')
    nil = facts.get('net_income_last')
    ffo = facts.get('net_income_current') + facts.get('depreciation')
    intwo = 1 if nic < 0 and nil < 0 else 0
    oeneg = 1 if tl > ta else 0
    chin = 0 if abs(nic) + abs(nil) == 0 else (nic - nil) / (abs(nic) + abs(nil))

    o_score = -1.32 - 0.407*math.log(ta / 1000) + 6.03*(tl / ta) - 1.43*(wc / ta) + 0.0757*(cl / ca) - 2.37*(nic / ta) - 1.83*(ffo / tl) + 0.285*intwo - 1.72*oeneg - 0.521*chin

    return o_score