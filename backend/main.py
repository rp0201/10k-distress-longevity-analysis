#!/usr/bin/env python3
"""FastAPI Backend for 10-K Distress Analysis"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.data.sec_client import SECClient
from src.parsers.parser import Parser
from src.models.bankruptcy_score import get_ohlson_oscore
from src.features.ratios_and_trends import (
    get_liquidity_ratios, 
    get_leverage_ratios, 
    get_profitability_ratios, 
    get_cash_flow_ratios,
    get_revenue_pct_change,
    get_net_income_pct_change
)
from src.scoring.composite_score import calculate_composite
from src.scoring.interpreter import get_recommendation

# Initialize FastAPI
app = FastAPI(
    title="10-K Distress Analysis API",
    description="Financial distress analysis using SEC 10-K data",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class AnalyzeRequest(BaseModel):
    ticker: str

class AnalysisResponse(BaseModel):
    ticker: str
    cik: str
    current_year: str
    prior_year: Optional[str]
    score: float
    grade: str
    risk_level: str
    recommendation: str
    alert_level: str
    hold_position: bool
    new_investment: bool
    metrics: dict
    financials: dict
    data_quality: dict

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if API is running"""
    return {"status": "ok", "message": "10-K Analysis API is running"}

# Main endpoint
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_ticker(request: AnalyzeRequest):
    """
    Analyze a company ticker for financial distress
    
    Returns comprehensive financial metrics, distress score, and investment recommendation
    """
    ticker = request.ticker.upper()
    
    try:
        # Fetch SEC data
        client = SECClient()
        cik = client.get_cik(ticker)
        
        if not cik:
            raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")
        
        data = client.get_latest_10k(ticker)
        
        # Parse data
        parser = Parser()
        parsed = parser.parse(data)
        
        # Check data quality
        filing_info = client.get_latest_10k_filing_info(ticker)
        is_stale = False
        filing_year = None
        data_fy = parsed.get('fiscal_years', {}).get('current_year')
        
        if filing_info and data_fy:
            filing_year = int(filing_info['reportDate'][:4])
            if (filing_year - data_fy) >= 2:
                is_stale = True
        
        # Get fiscal years
        fiscal_years = parsed.get('fiscal_years', {})
        current_fy = fiscal_years.get('current_year', 'N/A')
        prior_fy = fiscal_years.get('prior_year')
        
        # Combine facts
        facts = {}
        facts.update(parsed['balance_sheet'])
        facts.update(parsed['income_statement'])
        facts.update(parsed['cash_flow'])
        
        # Handle missing data
        if 'inventory' not in facts or facts['inventory'] is None:
            facts['inventory'] = 0
        if 'capital_expenditure' not in facts or facts['capital_expenditure'] is None:
            facts['capital_expenditure'] = 0
        
        # Check if financial institution missing key tags
        if 'current_assets' not in facts or 'current_liabilities' not in facts:
            raise HTTPException(
                status_code=400, 
                detail="Required financial data not found in 10-K filing. This typically occurs with banks, insurance companies, or incomplete filings."
            )
        
        # Calculate metrics
        o_score = get_ohlson_oscore(facts)
        liq = get_liquidity_ratios(facts)
        lev = get_leverage_ratios(facts)
        prof = get_profitability_ratios(facts)
        cf = get_cash_flow_ratios(facts)
        
        revenue_growth = get_revenue_pct_change(facts)
        ni_growth = get_net_income_pct_change(facts)
        
        # Composite score
        composite_result = calculate_composite(facts)
        score = composite_result['score']
        
        # Recommendation
        rec = get_recommendation(score)
        
        # Parse hold and new_investment responses
        hold_position = rec['hold'].lower() in ['yes', 'review']
        new_investment = rec['new_investment'].lower() in ['consider', 'maybe']
        
        # Build response
        return AnalysisResponse(
            ticker=ticker,
            cik=cik,
            current_year=f"FY{current_fy}",
            prior_year=f"FY{prior_fy}" if prior_fy else None,
            score=round(score, 2),
            grade=composite_result['grade'],
            risk_level=composite_result['risk_level'],
            recommendation=rec['rating'],
            alert_level=rec['alert_level'],
            hold_position=hold_position,
            new_investment=new_investment,
            metrics={
                "ohlson_o_score": round(o_score, 3),
                "current_ratio": round(liq['current_ratio'], 2),
                "quick_ratio": round(liq['quick_ratio'], 2),
                "debt_to_equity": round(lev['debt_to_equity'], 2),
                "interest_coverage": round(lev['interest_coverage_ratio'], 2),
                "roa": round(prof['ROA'], 2),
                "net_profit_margin": round(prof['net_profit_margin'], 3),
                "operating_cf_ratio": round(cf['operating_cash_flow'], 2),
                "free_cf_to_assets": round(cf['free_cash_flow_to_assets'], 3),
                "revenue_growth": round(revenue_growth, 2) if revenue_growth is not None else None,
                "net_income_growth": round(ni_growth, 2) if ni_growth is not None else None,
            },
            financials={
                "total_assets": facts.get('total_assets', 0),
                "revenue": facts.get('revenue_current', 0),
                "net_income": facts.get('net_income_current', 0),
                "operating_cash_flow": facts.get('operating_cash_flow', 0),
            },
            data_quality={
                "is_stale": is_stale,
                "filing_year": filing_year,
                "data_year": data_fy,
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
