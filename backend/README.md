# Backend - 10-K Financial Distress Analysis

Python-based backend for analyzing financial distress using SEC 10-K filings. Utilizes ratios and Ohlson O-score to determine investment risk and provides final reccomendation.

## TODO

### High Priority
- [ ] Reimplement test script

### Code Quality
- [ ] Improve error messages with more context
- [ ] Add logging throughout the application

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure SEC User-Agent (Required)
The SEC requires you to identify yourself when accessing their APIs. 

**Option A: Environment Variable (Recommended)**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your contact information
# SEC_USER_AGENT=YourAppName your.email@example.com
```

**Option B: Direct Configuration**
```python
from src.data.sec_client import SECClient

# Pass your user agent directly
client = SECClient(user_agent="MyApp myemail@example.com")
```

**Important**: Replace with your actual contact information. The SEC may block generic or fake user agents.
See: https://www.sec.gov/os/accessing-edgar-data

## Project Structure

The backend is organized into modular components:

```
backend/
├── main.py                    # FastAPI application entry point
├── config/
│   └── alt_tags.json          # Alternative tags configuration
├── src/
│   ├── data/
│   │   └── sec_client.py      # SEC EDGAR API client
│   ├── parsers/
│   │   └── parser.py          # Data extraction and fiscal year detection
│   ├── models/
│   │   └── bankruptcy_score.py # Ohlson O-Score calculation
│   ├── features/
│   │   └── ratios_and_trends.py # Financial ratios & percentage growth metrics
│   └── scoring/
│       ├── composite_score.py  # Composite distress score calculation
│       └── interpreter.py      # Score interpretation and recommendations
└── .env                       # Environment variables (not tracked)
```

## Core Functions

### SECClient (`src/data/sec_client.py`)
Handles all SEC EDGAR API interactions with configurable User-Agent.
- `get_cik(ticker)` - Convert ticker symbol to CIK (Central Index Key)
- `get_latest_10k(ticker)` - Fetch company facts JSON from SEC
- `get_latest_10k_filing_info(ticker)` - Get latest 10-K filing metadata (date, accession number)

### Parser (`src/parsers/parser.py`)
Extracts and normalizes financial data from SEC XBRL format.
- `parse(company_facts)` - Main parsing function
  - Uses alternative XBRL tags from `config/alt_tags.json`
  - Determines fiscal years for consistency across metrics
  - Returns: `{balance_sheet, income_statement, cash_flow, fiscal_years}`
- `_get_last_10k_value()` - Extract single most recent value for a metric
- `_get_current_and_prior_year_values()` - Extract two years for YoY comparison

### Financial Ratios (`src/features/ratios_and_trends.py`)
Calculates key financial health metrics.
- `get_liquidity_ratios(facts)` - Current ratio, quick ratio
- `get_leverage_ratios(facts)` - Debt-to-equity, interest coverage
- `get_profitability_ratios(facts)` - ROA, net profit margin
- `get_cash_flow_ratios(facts)` - Operating CF ratio, free CF to assets
- `get_revenue_pct_change(facts)` - Year-over-year revenue growth
- `get_net_income_pct_change(facts)` - Year-over-year net income growth

### Bankruptcy Model (`src/models/bankruptcy_score.py`)
Implements Ohlson O-Score bankruptcy prediction model.
- `get_ohlson_oscore(facts)` - Calculate O-Score using 9-factor formula
  - O > 0.5: High bankruptcy risk
  - O < 0.5: Low bankruptcy risk

### Composite Scoring (`src/scoring/composite_score.py`)
Aggregates all metrics into a single 0-100 distress score (lower is better).
- `calculate_composite(facts)` - Main scoring function
  - Normalizes all metrics to 0-100 scale
  - Applies weighted average (Ohlson 10%, Revenue Growth 15%, Cash Flow 12%, etc.)
  - Returns: `{score, grade, risk_level, interpretation, components}`

### Interpreter (`src/scoring/interpreter.py`)
Translates scores into actionable investment recommendations.
- `interpret_score(score)` - Convert score to grade (A-F) and risk level
- `get_recommendation(score)` - Generate buy/sell/hold advice with monitoring frequency

## Output Format

```python
{
    'score': 13.80,
    'grade': 'A',
    'risk_level': 'VERY LOW RISK',
    'interpretation': 'Strong financial health',
    'components': {
        'ohlson': {'score': 5.2, 'weight': 0.10, 'raw': -13.9},
        'revenue_growth': {'score': 2.1, 'weight': 0.15, 'raw': 114.2},
        # ... other components
    }
}
```

## Limitations

- **Stale Data**: SEC Company Facts API may have outdated data (5-15 years old)
- **Not Suitable For**: Banks, insurance companies, REITs (automatically detected and skipped)
- **Data Quality**: Some values may differ from actual 10-K filings

## Development

To add support for new XBRL tags, edit `config/alt_tags.json`:

```json
{
  "income_statement_tags": {
    "revenue": [
      "Revenues",
      "SalesRevenueNet",
      "YourNewTag"
    ]
  }
}
```