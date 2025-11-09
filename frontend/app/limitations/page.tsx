import { SiteHeader } from "@/components/site-header"
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"
import { AlertTriangle } from "lucide-react"

export default function LimitationsPage() {
  return (
    <div className="fixed inset-0 p-2 bg-[#0B0A09] font-sans">
      <div className="flex flex-col h-full w-full bg-[#12100E] rounded-lg border border-[#31302F] overflow-hidden">
        <div className="w-full px-4 md:px-8 py-2 border-b border-[#31302F] shrink-0">
          <SiteHeader />
        </div>

        <div className="flex-1 px-4 md:px-8 lg:px-40 xl:px-80 py-4 md:py-8 overflow-auto min-h-0">
          <div className="max-w-4xl mx-auto space-y-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">Limitations</h1>
          </div>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold border-b border-[#31302F] pb-2">SEC EDGAR API Constraints</h2>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-medium text-[#1A70A5] mb-2">Data Freshness</h3>
                <p className="text-gray-300 leading-relaxed">
                  The SEC Company Facts API may contain outdated data, sometimes ranging from 5-15 years old. 
                  This means the analysis might not reflect the company's current financial state. Always verify 
                  the fiscal year of the data being analyzed.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-medium text-[#1A70A5] mb-2">Tag Variations</h3>
                <p className="text-gray-300 leading-relaxed">
                  Companies use different tags for the same financial concepts. While we support multiple 
                  alternative tags, some companies may use non-standard tags that aren't captured, resulting in 
                  incomplete data extraction.
                </p>
              </div>
            </div>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold border-b border-[#31302F] pb-2">Company Type Restrictions</h2>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-medium text-[#1A70A5] mb-2">Financial Institutions</h3>
                <p className="text-gray-300 leading-relaxed">
                  Banks, insurance companies, and other financial institutions use different financial statement 
                  structures that don't align with our standard ratio calculations. These companies are excluded.
                </p>
              </div>
            </div>
          </section>

          <section className="space-y-4">
            <h2 className="text-2xl font-semibold border-b border-[#31302F] pb-2">Analytical Constraints</h2>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-medium text-[#1A70A5] mb-2">Historical Data Only</h3>
                <p className="text-gray-300 leading-relaxed">
                  Our analysis is based on historical 10-K filings and does not account for recent market events, 
                  management changes, or pending transactions that could significantly impact a company's prospects.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-medium text-[#1A70A5] mb-2">Industry Context</h3>
                <p className="text-gray-300 leading-relaxed">
                  The scoring system applies uniform thresholds across all industries. Some industries naturally 
                  operate with different leverage ratios, profitability margins, or cash flow patterns that may 
                  skew results.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-medium text-[#1A70A5] mb-2">Qualitative Factors</h3>
                <p className="text-gray-300 leading-relaxed">
                  Financial ratios cannot capture qualitative factors such as management quality, competitive 
                  positioning, brand value, or industry disruption risks that are crucial for investment decisions.
                </p>
              </div>
            </div>
          </section>
          </div>
        </div>
      </div>
    </div>
  )
}
