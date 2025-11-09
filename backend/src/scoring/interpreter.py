def interpret_score(score: float) -> dict:
    """
    Interpret composite distress score and assign grade, risk level, and interpretation.
    
    Args:
        score: Composite distress score (0-100, lower is better)
    
    Returns:
        dict with grade, risk_level, and interpretation
    """
    if score <= 20:
        grade = 'A'
        risk_level = 'Very Low Risk'
        interpretation = 'Strong financial health, solid fundamentals'
    elif score <= 35:
        grade = 'B'
        risk_level = 'Low Risk'
        interpretation = 'Generally healthy, minor concerns'
    elif score <= 50:
        grade = 'C'
        risk_level = 'Moderate Risk'
        interpretation = 'Warning signs present, operational challenges'
    elif score <= 65:
        grade = 'D'
        risk_level = 'High Risk'
        interpretation = 'Significant distress, deteriorating conditions'
    elif score <= 80:
        grade = 'E'
        risk_level = 'Very High Risk'
        interpretation = 'Severe financial distress, restructuring likely'
    else:
        grade = 'F'
        risk_level = 'Critical Risk'
        interpretation = 'Bankruptcy candidate, survival in question'
    
    return {
        'grade': grade,
        'risk_level': risk_level,
        'interpretation': interpretation
    }


def get_recommendation(score: float) -> dict:
    """
    Get investment recommendation based on distress score.
    
    Args:
        score: Composite distress score (0-100, lower is better)
    
    Returns:
        dict with rating, hold advice, new investment advice, and alert level
    """
    if score <= 20:
        return {
            'rating': 'Strong Buy',
            'hold': 'Yes',
            'new_investment': 'Consider',
            'alert_level': 'Quarterly'
        }
    elif score <= 35:
        return {
            'rating': 'Buy',
            'hold': 'Yes',
            'new_investment': 'Maybe',
            'alert_level': 'Quarterly'
        }
    elif score <= 50:
        return {
            'rating': 'Hold',
            'hold': 'Review',
            'new_investment': 'Avoid',
            'alert_level': 'Monthly'
        }
    elif score <= 65:
        return {
            'rating': 'Sell',
            'hold': 'Consider exit',
            'new_investment': 'No',
            'alert_level': 'Weekly'
        }
    elif score <= 80:
        return {
            'rating': 'Strong Sell',
            'hold': 'Exit',
            'new_investment': 'No',
            'alert_level': 'Daily'
        }
    else:
        return {
            'rating': 'Immediate Exit',
            'hold': 'Immediate exit',
            'new_investment': 'Never',
            'alert_level': 'Constant'
        }
