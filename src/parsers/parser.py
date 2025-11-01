from bs4 import BeautifulSoup
from lxml import etree

class HTMLPARSER:
    def parse(self, content: str) -> dict:
        soup = BeautifulSoup(content, 'lxml')

        return {
            'balance_sheet': self._extract_balance_sheet(soup),
            'income_statement': self._extract_income_statement(soup),
            'cash_flow': self._extract_cash_flow(soup),
            'mda': self._extract_mda(soup)

        }

    def _extract_balance_sheet(self, soup):
        pass

    def _extract_income_statement(self, soup):
        pass

    def _extract_cash_flow(self, soup):
        data = {}



    def _extract_mda(self, soup):
        pass
