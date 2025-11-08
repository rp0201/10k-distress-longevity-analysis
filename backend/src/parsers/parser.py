
import json
import os

class Parser:
    def __init__(self):
        self.current_fiscal_year = None
        self.prior_fiscal_year = None
        self.alt_tags = self._load_alt_tags()
    
    def _load_alt_tags(self):
        """
        Load alternative tags from config file
        """
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'alt_tags.json')
        try:
            with open(config_path) as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load alt_tags.json: {e}")
            return {}
    
    def parse(self, company_facts: dict) -> dict:
        """
        Returns parsed financials
        """
        us_gaap_facts = company_facts['facts'].get('us-gaap', {})
        
        # Determine fiscal years first to ensure consistency
        self._determine_fiscal_years(us_gaap_facts)

        return {
            'balance_sheet': self._extract_balance_sheet(us_gaap_facts),
            'income_statement': self._extract_income_statement(us_gaap_facts),
            'cash_flow': self._extract_cash_flow(us_gaap_facts),
            'fiscal_years': {
                'current_year': self.current_fiscal_year,
                'prior_year': self.prior_fiscal_year
            },
        }
    
    def _determine_fiscal_years(self, facts: dict):
        """Determine the most recent fiscal years from the data to ensure consistency"""
        # Try to get years from revenue data (most reliable)
        revenue_tags = self.alt_tags.get('income_statement_tags', {}).get('revenue', ['Revenues'])
        
        for tag in revenue_tags:
            if tag in facts:
                concept = facts[tag]
                units = concept.get('units', {})
                
                # Find USD unit
                unit_key = 'USD'
                if unit_key not in units:
                    for u in units.keys():
                        if 'usd' in u.lower():
                            unit_key = u
                            break
                
                if unit_key in units:
                    all_facts = units[unit_key]
                    ten_k_facts = [f for f in all_facts if f.get('form') in ('10-K', '10-K/A')]
                    
                    if ten_k_facts:
                        fy_facts = {}
                        for f in ten_k_facts:
                            fy = f.get('fy')
                            if fy is not None:
                                try:
                                    fy_int = int(fy)
                                    if fy_int not in fy_facts or f.get('end', '') > fy_facts[fy_int].get('end', ''):
                                        fy_facts[fy_int] = f
                                except Exception:
                                    pass
                        
                        if len(fy_facts) >= 1:
                            sorted_years = sorted(fy_facts.keys(), reverse=True)
                            self.current_fiscal_year = sorted_years[0]
                            if len(sorted_years) > 1:
                                self.prior_fiscal_year = sorted_years[1]
                            return
        
        # Try to find any fiscal year data
        self.current_fiscal_year = None
        self.prior_fiscal_year = None

    def _try_alternative_tags(self, facts: dict, field_name: str, category: str, unit: str = 'USD', is_annual: bool = False):
        """
        Try multiple alt tags for a given field
        """
        alt_tags = self.alt_tags.get(category, {}).get(field_name, [])
        
        for tag in alt_tags:
            value = self._get_last_10k_value(facts, tag, unit, is_annual)
            if value is not None:
                return value
        return None
    
    def _extract_multi_year_field(self, facts: dict, field_name: str, category: str, result: dict):
        """
        Extract both current and prior year values for a field
        """
        tags = self.alt_tags.get(category, {}).get(field_name, [])
        current, prior = None, None
        
        for tag in tags:
            current, prior = self._get_current_and_prior_year_values(facts, tag, 'USD')
            if current is not None:
                break
        
        if current is not None:
            result[f'{field_name}_current'] = current
            result[field_name] = current
        if prior is not None:
            result[f'{field_name}_last'] = prior

    def _extract_balance_sheet(self, facts: dict):
        """
        Extract balance sheet data using alternative tags
        """
        result = {}
        
        # Standard fields associated with balance sheet
        fields = {
            'total_assets': ('USD', False),
            'current_assets': ('USD', False),
            'cash': ('USD', False),
            'short_term_investments': ('USD', False),
            'accounts_receivable': ('USD', False),
            'inventory': ('USD', False),
            'total_liabilities': ('USD', False),
            'current_liabilities': ('USD', False),
            'stockholders_equity': ('USD', False),
            'retained_earnings': ('USD', False),
            'capital_expenditures': ('USD', False),
        }
        
        for field, (unit, is_annual) in fields.items():
            value = self._try_alternative_tags(facts, field, 'balance_sheet_tags', unit, is_annual)
            if value is not None:
                result[field] = value
        
        # If total_liabilities is still missing, try to calculate from components
        if 'total_liabilities' not in result:
            current_liab = result.get('current_liabilities')
            noncurrent_tags = [
                'LiabilitiesNoncurrent',
                'LiabilitiesAndStockholdersEquity', 
                'LongTermDebt',
                'LiabilitiesOtherThanLongtermDebtNoncurrent'
            ]
            
            noncurrent_liab = None
            for tag in noncurrent_tags:
                noncurrent_liab = self._get_last_10k_value(facts, tag, 'USD', is_annual=False)
                if noncurrent_liab:
                    break
            
            if current_liab and noncurrent_liab:
                result['total_liabilities'] = current_liab + noncurrent_liab
            
        return result

    def _extract_income_statement(self, facts: dict):
        """
        Extract income statement data using alternative tags
        """
        result = {}
        
        # Standard fields with default unit and annual flag
        fields = {
            'cost_of_goods_sold': ('USD', True),
            'gross_profit': ('USD', True),
            'operating_income': ('USD', True),
            'operating_expenses': ('USD', True),
            'interest_expense': ('USD', True),
        }
        
        for field, (unit, is_annual) in fields.items():
            value = self._try_alternative_tags(facts, field, 'income_statement_tags', unit, is_annual)
            if value is not None:
                result[field] = value
        
        # Handle EPS with multiple unit formats
        for unit in ['USD/shares', 'USD/share', 'USD']:
            value = self._try_alternative_tags(facts, 'earnings_per_share', 'income_statement_tags', unit, is_annual=True)
            if value is not None:
                result['earnings_per_share'] = value
                break
        
        # Get multi-year fields (net income and revenue)
        self._extract_multi_year_field(facts, 'net_income', 'income_statement_tags', result)
        self._extract_multi_year_field(facts, 'revenue', 'income_statement_tags', result)

        return result

    def _extract_cash_flow(self, facts: dict):
        """Extract cash flow data using alternative tags"""
        result = {}
        
        # Standard fields with default unit and annual flag, plus output key mapping
        fields = {
            'operating_cf': ('USD', True, 'operating_cash_flow'),
            'investing_cf': ('USD', True, 'investing_cash_flow'),
            'financing_cf': ('USD', True, 'financing_cash_flow'),
            'depreciation': ('USD', True, 'depreciation'),
        }
        
        for field, (unit, is_annual, result_key) in fields.items():
            value = self._try_alternative_tags(facts, field, 'cashflow_tags', unit, is_annual)
            if value is not None:
                result[result_key] = value

        return result

    def _get_last_10k_value(self, facts: dict, tag: str, unit: str = 'USD', is_annual: bool = True) -> float:
        """
        Extract the most recent single value for a specific tag from 10-K filings
        """
        if tag not in facts:
            return None
        
        concept = facts[tag]
        units = concept.get('units', {})
        if unit in units:
            all_facts = units[unit]
        else:
            chosen = None
            for u in units.keys():
                if 'usd' in u.lower():
                    chosen = u
                    break
            if chosen is None:
                try:
                    chosen = list(units.keys())[0]
                except Exception:
                    return None
            all_facts = units[chosen]

        ten_k_facts = [f for f in all_facts if f.get('form') in ('10-K', '10-K/A')]
        if not ten_k_facts:
            ten_k_facts = list(all_facts)

        if not ten_k_facts:
            return None

        # Use the determined fiscal year if available
        if self.current_fiscal_year is not None:
            # Filter to current fiscal year
            fy_filtered = [f for f in ten_k_facts 
                          if f.get('fy') is not None 
                          and int(f.get('fy')) == self.current_fiscal_year]
            if fy_filtered:
                # Sort by end date and filed date to get most recent within the fiscal year
                def sort_key(f):
                    end = f.get('end', '') or ''
                    filed = f.get('filed', '') or ''
                    return (end, filed)
                
                fy_filtered.sort(key=sort_key, reverse=True)
                return fy_filtered[0].get('val')
        
        # Fallback to old logic if no fiscal year determined
        fy_vals = []
        for f in ten_k_facts:
            fy = f.get('fy')
            if fy is not None:
                try:
                    fy_vals.append(int(fy))
                except Exception:
                    pass

        if fy_vals:
            max_fy = max(fy_vals)
            fy_filtered = [f for f in ten_k_facts if f.get('fy') is not None and int(f.get('fy')) == max_fy]
            if fy_filtered:
                ten_k_facts = fy_filtered
        else:
            if is_annual:
                annual_candidates = []
                import datetime
                for f in ten_k_facts:
                    end = f.get('end', '')
                    start = f.get('start', '')
                    if isinstance(end, str) and end.endswith('-12-31'):
                        annual_candidates.append(f)
                        continue
                    if start and end:
                        try:
                            sd = datetime.date.fromisoformat(start)
                            ed = datetime.date.fromisoformat(end)
                            if (ed - sd).days >= 350:
                                annual_candidates.append(f)
                        except Exception:
                            pass
                if annual_candidates:
                    ten_k_facts = annual_candidates

        if not ten_k_facts:
            return None

        def sort_key(f):
            fy = f.get('fy')
            try:
                fyv = int(fy) if fy is not None else 0
            except Exception:
                fyv = 0
            end = f.get('end', '') or ''
            filed = f.get('filed', '') or ''
            return (fyv, end, filed)

        ten_k_facts.sort(key=sort_key, reverse=True)

        return ten_k_facts[0].get('val')

    def _get_current_and_prior_year_values(self, facts: dict, tag: str, unit: str = 'USD'):
        """
        Extract both current and prior fiscal year values for a specific tag
        """
        if tag not in facts:
            return None, None
        
        concept = facts[tag]
        
        units = concept.get('units', {})
        if unit in units:
            all_facts = units[unit]
        else:
            chosen = None
            for u in units.keys():
                if 'usd' in u.lower():
                    chosen = u
                    break
            if chosen is None:
                try:
                    chosen = list(units.keys())[0]
                except Exception:
                    return None, None
            all_facts = units[chosen]

        ten_k_facts = [f for f in all_facts if f.get('form') in ('10-K', '10-K/A')]
        if not ten_k_facts:
            ten_k_facts = list(all_facts)

        if not ten_k_facts:
            return None, None

        fy_facts = {}
        for f in ten_k_facts:
            fy = f.get('fy')
            if fy is not None:
                try:
                    fy_int = int(fy)
                    if fy_int not in fy_facts or f.get('end', '') > fy_facts[fy_int].get('end', ''):
                        fy_facts[fy_int] = f
                except Exception:
                    pass

        if len(fy_facts) < 1:
            return None, None

        sorted_years = sorted(fy_facts.keys(), reverse=True)
        
        current_year = sorted_years[0]
        current_value = fy_facts[current_year].get('val')
        
        prior_value = None
        if len(sorted_years) > 1:
            prior_year = sorted_years[1]
            prior_value = fy_facts[prior_year].get('val')

        return current_value, prior_value
