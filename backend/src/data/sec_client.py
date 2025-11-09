import requests
import os

class SECClient:
    def __init__(self, user_agent: str = None):
        """
        Use provided user agent or fall back to environment variable
        Users should set SEC_USER_AGENT env var with their contact info
        """
        if user_agent is None:
            user_agent = os.getenv(
                'SEC_USER_AGENT',
                '10K-Distress-Analysis YourEmail@example.com'
            )
        
        self.headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate'
        }

        self.cik_map = self._load_cik_map()

    def _load_cik_map(self):
        """
        Loads all CIK's
        """
        url = "https://www.sec.gov/files/company_tickers.json"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception:
            return {}

        mapping = {}

        for company in data.values():
            ticker = company.get('ticker')
            cik_str = company.get('cik_str')
            if not ticker or cik_str is None:
                continue

            # SEC CIKs are 10 digits
            cik = str(cik_str).zfill(10)
            mapping[ticker.upper()] = cik

        return mapping

    def get_cik(self, ticker: str) -> str:
        """
        Find CIK from ticker in map
        """
        ticker = ticker.upper()

        if not self.cik_map or ticker not in self.cik_map:
            raise ValueError(f"Ticker {ticker} not in mapping...")

        return self.cik_map[ticker]

    def get_latest_10k(self, ticker: str) -> dict:
        """
        Get the latest 10-K data from SEC Company Facts API
        Note: Some companies have outdated company facts
        """
        cik = self.get_cik(ticker)
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()

        return response.json()
    
    def _get_recent_filings(self, ticker: str) -> dict:
        """
        Get recent filings from submissions endpoint
        Returns the submissions data which includes recent 10-K filings
        """
        cik = self.get_cik(ticker)
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"

        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()

        return response.json()
    
    def get_latest_10k_filing_info(self, ticker: str) -> dict:
        """
        Get information about the most recent 10-K filing
        Returns dict with accessionNumber, filingDate, reportDate, form
        """
        submissions = self._get_recent_filings(ticker)
        
        # Get recent filings from the 'filings' -> 'recent' section
        recent = submissions.get('filings', {}).get('recent', {})
        
        if not recent:
            return None
        
        # Extract arrays
        forms = recent.get('form', [])
        accession_numbers = recent.get('accessionNumber', [])
        filing_dates = recent.get('filingDate', [])
        report_dates = recent.get('reportDate', [])
        
        # Find the most recent 10-K or 10-K/A
        for i, form in enumerate(forms):
            if form in ('10-K', '10-K/A'):
                return {
                    'form': form,
                    'accessionNumber': accession_numbers[i],
                    'filingDate': filing_dates[i],
                    'reportDate': report_dates[i]
                }
        
        return None