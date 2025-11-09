"use client"

import { useState, useEffect } from "react"
import { toast } from "sonner"
import { Toaster } from "@/components/ui/sonner"
import { SiteHeader } from "@/components/site-header"
import { ExportTable } from "@/components/output-table"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle } from "lucide-react"

export interface CompanyAnalysis {
  ticker: string
  cik: string
  current_year: string
  prior_year: string | null
  score: number
  grade: string
  risk_level: string
  recommendation: string
  alert_level: string
  hold_position: boolean
  new_investment: boolean
  metrics: {
    ohlson_o_score: number
    current_ratio: number
    quick_ratio: number
    debt_to_equity: number
    interest_coverage: number
    roa: number
    net_profit_margin: number
    operating_cf_ratio: number
    free_cf_to_assets: number
    revenue_growth: number | null
    net_income_growth: number | null
  }
  financials: {
    total_assets: number
    revenue: number
    net_income: number
    operating_cash_flow: number
  }
  data_quality: {
    is_stale: boolean
    filing_year: number | null
    data_year: number
  }
}

export default function Home() {
  const [companies, setCompanies] = useState<CompanyAnalysis[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isInitialized, setIsInitialized] = useState(false)

  // Load companies from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('analyzedCompanies')
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        setCompanies(parsed)
      } catch (e) {
        console.error('Failed to parse saved companies:', e)
      }
    }
    setIsInitialized(true)
  }, [])

  // Save companies to localStorage whenever it changes (after initialization)
  useEffect(() => {
    if (isInitialized) {
      localStorage.setItem('analyzedCompanies', JSON.stringify(companies))
    }
  }, [companies, isInitialized])

  const analyzeTickers = async (tickers: string[]) => {
    // Remove duplicates (case-insensitive)
    const uniqueTickers = Array.from(new Set(tickers.map(t => t.toUpperCase())))
    
    // Filter out tickers already in the companies list
    const existingTickers = new Set(companies.map(c => c.ticker.toUpperCase()))
    const newTickers = uniqueTickers.filter(t => !existingTickers.has(t))
    
    if (newTickers.length === 0) {
      toast.error("No new tickers", {
        description: "Entered ticker has already been analyzed."
      })
      return
    }
    
    setLoading(true)
    setError(null)
    
    // Analyze tickers one by one
    let successCount = 0
    for (const ticker of newTickers) {
      try {
        const response = await fetch('http://localhost:8000/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ ticker: ticker }),
        })

        if (!response.ok) {
          if (response.status === 400) {
            const errorData = await response.json()
            toast.error(`Cannot analyze ${ticker}`, {
              description: errorData.detail || "Required financial data not available in 10-K filing."
            })
            continue
          } else if (response.status === 404) {
            toast.error(`${ticker} not found`, {
              description: "Ticker symbol could not be found. Please check and try again."
            })
            continue
          }
          throw new Error('Failed to analyze ticker')
        }

        const data: CompanyAnalysis = await response.json()
        
        // Add the new company to the list immediately
        setCompanies(prev => [...prev, data])
        successCount++
        
        // Show individual success toast
        toast.success(`${ticker} analyzed`, {
          description: `Grade: ${data.grade} - ${data.recommendation}`
        })
      } catch (err) {
        console.error(`Error analyzing ${ticker}:`, err)
        toast.error(`Failed to analyze ${ticker}`, {
          description: "Connection error or server issue."
        })
      }
    }
    
    setLoading(false)
    
    // Final summary if multiple tickers
    if (newTickers.length > 1) {
      toast.success("Batch analysis complete", {
        description: `Successfully analyzed ${successCount} of ${newTickers.length} tickers`
      })
    }
  }

  const handleClear = () => {
    setCompanies([])
    toast.success("Cleared all analyses")
  }

  return (
    <div className="fixed inset-0 p-2 bg-[#0B0A09] font-sans">
      <Toaster position="top-right" theme="dark" />
      <div className="flex flex-col h-full w-full bg-[#12100E] rounded-lg border border-[#31302F] overflow-hidden">
        <div className="w-full px-4 md:px-8 py-2 border-b border-[#31302F] shrink-0">
          <SiteHeader/>
        </div>
        <div className="flex-1 px-4 md:px-8 lg:px-40 xl:px-80 py-4 md:py-8 overflow-auto min-h-0">
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          <ExportTable 
            companies={companies} 
            onClear={handleClear}
            onAnalyze={analyzeTickers}
            disabled={loading}
          />
        </div>
      </div>
    </div>
  );
}
