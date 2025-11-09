"use client"

import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import type { CompanyAnalysis } from "@/app/page"
import Image from "next/image"

interface ExportTableProps {
  companies: CompanyAnalysis[]
  onClear: () => void
  onAnalyze: (tickers: string[]) => Promise<void>
  disabled?: boolean
}

// Helper function to format large numbers
function formatCurrency(value: number): string {
  const absValue = Math.abs(value)
  
  if (absValue >= 1e12) {
    return `$${(value / 1e12).toFixed(2)}T`
  } else if (absValue >= 1e9) {
    return `$${(value / 1e9).toFixed(2)}B`
  } else if (absValue >= 1e6) {
    return `$${(value / 1e6).toFixed(2)}M`
  } else {
    return `$${value.toFixed(2)}`
  }
}

// Helper function to format fiscal years for mobile
function formatYear(year: string): string {
  // Convert "FY2024" to "24", "FY2023" to "23", etc.
  if (year.startsWith('FY')) {
    return year.slice(-2) // Get last 2 characters
  }
  // Handle edge cases like "ne" or invalid formats
  if (year.length === 2 && !isNaN(parseInt(year))) {
    return year
  }
  return year.slice(-2) || 'NA'
}

// Helper function to format year range (always prior-current, older to newer)
function formatYearRange(currentYear: string, priorYear: string | null): string {
  const currentYearFormatted = formatYear(currentYear)
  if (!priorYear || priorYear === "N/A") {
    return `NA-${currentYearFormatted}`
  }
  const priorYearFormatted = formatYear(priorYear)
  return `${priorYearFormatted}-${currentYearFormatted}`
}

export function ExportTable({ companies, onClear, onAnalyze, disabled = false }: ExportTableProps) {
  const [selectedCompany, setSelectedCompany] = useState<CompanyAnalysis | null>(null)
  const [input, setInput] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!input.trim()) return
    
    const tickers = input
      .split(",")
      .map(t => t.trim().toUpperCase())
      .filter(t => t.length > 0)
    
    if (tickers.length > 0) {
      await onAnalyze(tickers)
      setInput("")
    }
  }

  if (companies.length === 0) {
    return (
      <div className="space-y-6">
        {/* Input Form */}
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row justify-center w-full gap-3">
          <Input 
            type="text" 
            placeholder="TICK, TICK, TICK… (e.g. NVDA, ORCL)" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={disabled}
            className="flex-1 text-base"
          />
          <div className="flex gap-3 w-full sm:w-auto">
            <Button 
              type="submit" 
              variant="outline"
              disabled={disabled || !input.trim()}
              className="flex-1 sm:flex-none sm:w-auto"
            >
              {disabled ? "Analyzing" : "Start"}
            </Button>
            <Button 
              type="button"
              variant="outline" 
              onClick={onClear}
              disabled={companies.length === 0}
              className="flex-1 sm:flex-none sm:w-auto border-[#31302F] text-gray-300 hover:bg-[#1A1817] hover:text-white disabled:opacity-50"
            >
              Clear All
            </Button>
          </div>
        </form>

        {/* Empty State */}
        <div className="flex flex-col items-center justify-center text-center text-gray-400 py-12 space-y-4 select-none">
          <Image 
            src="/empty_state.svg"
            alt="Empty State"
            width={280}
            height={280}
            className="opacity-50 pointer-events-none"
          />
          <div className="space-y-2">
            <h3 className="text-4 font-medium text-[#303030]">There's nothing here!</h3>
            <p className="text-3 text-[#4F4C48]">There are no financials to review right now. Try entering some tickers!</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row justify-center w-full gap-3">
        <Input 
          type="text" 
          placeholder="TICK, TICK, TICK… (e.g. NVDA, ORCL)" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={disabled}
          className="flex-1 text-base"
        />
        <div className="flex gap-3 w-full sm:w-auto">
          <Button 
            type="submit" 
            variant="outline"
            disabled={disabled || !input.trim()}
            className="flex-1 sm:flex-none sm:w-auto"
          >
            {disabled ? "Analyzing" : "Start"}
          </Button>
          <Button 
            type="button"
            variant="outline" 
            onClick={onClear}
            disabled={companies.length === 0}
            className="flex-1 sm:flex-none sm:w-auto border-[#31302F] text-gray-300 hover:bg-[#1A1817] hover:text-white disabled:opacity-50"
          >
            Clear All
          </Button>
        </div>
      </form>

      {/* Table with sticky header */}
      <div className="rounded-md border border-[#31302F] w-full max-h-[calc(100vh-20rem)] overflow-auto">
        <table className="w-full caption-bottom text-sm">
          <thead className="sticky top-0 bg-[#12100E] z-10 shadow-[0_1px_0_0_#31302F]">
            <tr>
              <th className="text-gray-300 whitespace-nowrap bg-[#12100E] h-10 px-2 text-left align-middle font-medium">Ticker</th>
              <th className="text-gray-300 bg-[#12100E] h-10 px-2 text-left align-middle font-medium">Year</th>
              <th className="text-gray-300 hidden md:table-cell bg-[#12100E] h-10 px-2 text-left align-middle font-medium">CIK</th>
              <th className="text-left text-gray-300 bg-[#12100E] h-10 px-2 align-middle font-medium">Action</th>
            </tr>
          </thead>
          <tbody>
          {companies.map((company) => (
            <tr key={company.cik} className="border-b border-[#31302F] hover:bg-muted/50 transition-colors">
              <td className="p-2 align-middle font-medium text-white whitespace-nowrap">{company.ticker}</td>
              <td className="p-2 align-middle text-gray-300 whitespace-nowrap">
                {formatYearRange(company.current_year, company.prior_year)}
              </td>
              <td className="p-2 align-middle text-gray-300 hidden md:table-cell">{company.cik}</td>
              <td className="p-2 align-middle text-left">
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="link" size="sm" onClick={() => setSelectedCompany(company)} className="text-xs sm:text-sm whitespace-nowrap">
                      <span className="hidden sm:inline">View Analysis</span>
                      <span className="sm:hidden">Details</span>
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-[95vw] sm:max-w-4xl max-h-[85vh] sm:max-h-[80vh] overflow-y-auto bg-[#12100E] border-[#31302F]">
                    <DialogHeader>
                      <DialogTitle className="text-xl sm:text-2xl text-white">
                        {company.ticker} - Comprehensive Analysis
                      </DialogTitle>
                    </DialogHeader>
                    
                    {selectedCompany && (
                      <div className="space-y-4 sm:space-y-6 mt-4">
                        {/* Composite Score Section */}
                        <div className="bg-[#1A1816] p-3 sm:p-4 rounded-lg border border-[#31302F]">
                          <h3 className="text-base sm:text-lg font-semibold mb-2 text-white">Composite Score</h3>
                          <div className="grid grid-cols-2 gap-3 sm:gap-4">
                            <div>
                              <p className="text-xs sm:text-sm text-gray-400">Score</p>
                              <p className="text-xl sm:text-2xl font-bold text-white">{selectedCompany.score}/100</p>
                            </div>
                            <div>
                              <p className="text-xs sm:text-sm text-gray-400">Grade</p>
                              <p className="text-xl sm:text-2xl font-bold text-white">{selectedCompany.grade}</p>
                            </div>
                            <div>
                              <p className="text-xs sm:text-sm text-gray-400">Risk Level</p>
                              <p className="text-sm sm:text-lg text-white">{selectedCompany.risk_level}</p>
                            </div>
                            <div>
                              <p className="text-xs sm:text-sm text-gray-400">Recommendation</p>
                              <p className="text-sm sm:text-lg font-semibold text-white">{selectedCompany.recommendation}</p>
                            </div>
                          </div>
                        </div>

                        {/* Financials Section */}
                        <div>
                          <h3 className="text-base sm:text-lg font-semibold mb-2 text-white">Key Financials</h3>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3 text-xs sm:text-sm">
                            <div>
                              <p className="text-gray-400">Total Assets</p>
                              <p className="font-medium text-white">{formatCurrency(selectedCompany.financials.total_assets)}</p>
                            </div>
                            <div>
                              <p className="text-gray-400">Revenue</p>
                              <p className="font-medium text-white">{formatCurrency(selectedCompany.financials.revenue)}</p>
                            </div>
                            <div>
                              <p className="text-gray-400">Net Income</p>
                              <p className="font-medium text-white">{formatCurrency(selectedCompany.financials.net_income)}</p>
                            </div>
                            <div>
                              <p className="text-gray-400">Operating Cash Flow</p>
                              <p className="font-medium text-white">{formatCurrency(selectedCompany.financials.operating_cash_flow)}</p>
                            </div>
                          </div>
                        </div>

                        {/* Metrics Section */}
                        <div>
                          <h3 className="text-base sm:text-lg font-semibold mb-2 text-white">Financial Metrics</h3>
                          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 sm:gap-3 text-xs sm:text-sm">
                            <div>
                              <p className="text-gray-400">Ohlson O-Score</p>
                              <p className="font-medium text-white">{selectedCompany.metrics.ohlson_o_score.toFixed(3)}</p>
                            </div>
                            <div>
                              <p className="text-gray-400">Current Ratio</p>
                              <p className="font-medium text-white">{selectedCompany.metrics.current_ratio.toFixed(2)}</p>
                            </div>
                            <div>
                              <p className="text-gray-400">Quick Ratio</p>
                              <p className="font-medium text-white">{selectedCompany.metrics.quick_ratio.toFixed(2)}</p>
                            </div>
                            <div>
                              <p className="text-gray-400">Debt-to-Equity</p>
                              <p className="font-medium text-white">{selectedCompany.metrics.debt_to_equity.toFixed(2)}</p>
                            </div>
                            <div>
                              <p className="text-gray-400">Interest Coverage</p>
                              <p className="font-medium text-white">{selectedCompany.metrics.interest_coverage.toFixed(2)}</p>
                            </div>
                            <div>
                              <p className="text-gray-400">ROA</p>
                              <p className="font-medium text-white">{selectedCompany.metrics.roa.toFixed(2)}%</p>
                            </div>
                            <div>
                              <p className="text-gray-400">Net Profit Margin</p>
                              <p className="font-medium text-white">{selectedCompany.metrics.net_profit_margin.toFixed(3)}</p>
                            </div>
                            <div>
                              <p className="text-gray-400">Operating CF Ratio</p>
                              <p className="font-medium text-white">{selectedCompany.metrics.operating_cf_ratio.toFixed(2)}</p>
                            </div>
                            <div>
                              <p className="text-gray-400">Free CF to Assets</p>
                              <p className="font-medium text-white">{selectedCompany.metrics.free_cf_to_assets.toFixed(3)}</p>
                            </div>
                          </div>
                        </div>

                        {/* Growth Section */}
                        <div>
                          <h3 className="text-base sm:text-lg font-semibold mb-2 text-white">Growth Metrics</h3>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3 text-xs sm:text-sm">
                            <div>
                              <p className="text-gray-400">Revenue Growth</p>
                              <p className="font-medium text-white">
                                {selectedCompany.metrics.revenue_growth !== null 
                                  ? `${selectedCompany.metrics.revenue_growth > 0 ? '+' : ''}${selectedCompany.metrics.revenue_growth.toFixed(2)}%`
                                  : 'N/A'}
                              </p>
                            </div>
                            <div>
                              <p className="text-gray-400">Net Income Growth</p>
                              <p className="font-medium text-white">
                                {selectedCompany.metrics.net_income_growth !== null 
                                  ? `${selectedCompany.metrics.net_income_growth > 0 ? '+' : ''}${selectedCompany.metrics.net_income_growth.toFixed(2)}%`
                                  : 'N/A'}
                              </p>
                            </div>
                          </div>
                        </div>

                        {/* Data Quality Warning */}
                        {selectedCompany.data_quality.is_stale && (
                          <div className="bg-yellow-900/20 border border-yellow-800 p-3 rounded-lg">
                            <p className="text-xs sm:text-sm text-yellow-200">
                              ⚠️ Data Quality Warning: This data is from FY{selectedCompany.data_quality.data_year}, 
                              which is {selectedCompany.data_quality.filing_year! - selectedCompany.data_quality.data_year} years outdated.
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </DialogContent>
                </Dialog>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
    </div>
  )
}
