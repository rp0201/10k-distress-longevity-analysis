import requests

class SECCLIENT:
    def __init__(self):

        self.headers = {
            'User-Agent': 'Name / Contact: example@domain.com (temporary dev)',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate'
        }

        self.cik_map = self._load_cik_map()


    def _load_cik_map(self):

        url = "https://www.sec.gov/files/company_tickers.json"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception:
            # If the request fails, return an empty mapping so the rest of the
            # program can run and surface a clearer error later.
            return {}

        mapping = {}

        for company in data.values():
            # be defensive about missing keys
            ticker = company.get('ticker')
            cik_str = company.get('cik_str')
            if not ticker or cik_str is None:
                continue

            # SEC CIKs are typically zero-padded to 10 digits
            cik = str(cik_str).zfill(10)
            mapping[ticker.upper()] = cik

        return mapping

    def get_cik(self, ticker: str) -> str:

        ticker = ticker.upper()

        if not self.cik_map or ticker not in self.cik_map:
            raise ValueError(f"Ticker {ticker} not in mapping...")

        return self.cik_map[ticker]

    def get_latest_10k(self, ticker: str) -> dict:
        cik = self.get_cik(ticker)
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()

        return response.json()