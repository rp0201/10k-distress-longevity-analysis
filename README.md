# 10-K Financial Distress Analysis

> 🚀 **Open Source** | Automated financial distress scoring using SEC 10-K filings

Comprehensive financial analysis tool that calculates a composite risk score (0-100) based on 11 financial metrics including Ohlson O-Score, liquidity ratios, leverage, profitability, and cash flow analysis.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/rp0201/10k-distress-longevity-analysis)

## 🎯 Features

- **Composite Distress Score**: 0-100 scale with letter grades (A-F)
- **11 Financial Metrics**: Comprehensive analysis including Ohlson O-Score, growth rates, and ratios
- **Multi-Company Analysis**: Analyze multiple tickers simultaneously
- **Real-time Analysis**: Instant results from SEC EDGAR API
- **Data Quality Warnings**: Automatic alerts for stale or outdated data
- **Persistent Storage**: Save your analyses across sessions
- **Responsive Design**: Works on desktop and mobile devices
- **Open Source**: MIT licensed, contributions welcome

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Set up SEC User-Agent (required for API access)
cp .env.example .env
# Edit .env and add your contact info

# Run FastAPI server
fastapi dev main.py
# Server runs on http://localhost:8000
```

### Frontend Setup
```bash
cd frontend
npm install

# Configure API endpoint
cp .env.example .env.local
# Edit .env.local: NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
# Open http://localhost:3000
```

## 📁 Project Structure

```
10k-distress-longevity-analysis/
├── backend/              # Python FastAPI analysis engine
│   ├── src/             # Core modules
│   │   ├── data/        # SEC API client
│   │   ├── parsers/     # XBRL parsing
│   │   ├── models/      # Bankruptcy models
│   │   ├── features/    # Financial metrics
│   │   └── scoring/     # Composite scoring
│   ├── config/          # Alternative XBRL tags
│   ├── main.py          # FastAPI application
│   └── requirements.txt
├── frontend/            # Next.js web application
│   ├── app/            # Next.js App Router
│   │   ├── page.tsx    # Home page
│   │   └── limitations/ # Documentation
│   ├── components/     # React components
│   │   ├── site-header.tsx
│   │   ├── output-table.tsx
│   │   └── ui/         # shadcn/ui components
│   ├── public/         # Static assets
│   └── package.json
└── README.md           # This file
```

## 📊 Scoring System

### Composite Score (0-100, lower is better)
| Grade | Range | Risk Level | Action |
|-------|-------|------------|--------|
| **A** | 0-20 | Very Low Risk | Strong Buy |
| **B** | 21-35 | Low Risk | Buy |
| **C** | 36-50 | Moderate Risk | Hold |
| **D** | 51-65 | High Risk | Sell |
| **E** | 66-80 | Very High Risk | Strong Sell |
| **F** | 81-100 | Critical Risk | Immediate Exit |

### Metrics & Weights
| Metric | Weight | Description |
|--------|--------|-------------|
| Ohlson O-Score | 10% | Bankruptcy probability model |
| Revenue Growth | 15% | Year-over-year revenue change |
| Net Income Growth | 15% | Year-over-year profit change |
| Operating Cash Flow | 12% | Cash generation capability |
| Free Cash Flow | 8% | Available cash after investments |
| Current Ratio | 8% | Short-term liquidity |
| Quick Ratio | 7% | Immediate liquidity |
| Debt-to-Equity | 8% | Financial leverage |
| Interest Coverage | 7% | Debt servicing ability |
| Return on Assets | 5% | Asset efficiency |
| Net Profit Margin | 5% | Profitability |

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Data Source**: SEC EDGAR Company Facts API
- **Parsing**: XBRL with alternative tag support
- **Models**: Ohlson O-Score, custom composite scoring

### Frontend
- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Icons**: Lucide React
- **Notifications**: Sonner (Toast)
- **State**: React Hooks + localStorage

## 🚀 Deployment

### Frontend (Vercel) - Recommended

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Set root directory: `frontend`

3. **Configure Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` with your backend URL

4. **Deploy!** 🎉

### Backend Options

**Option 1: Railway**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
cd backend
railway login
railway init
railway up
```

**Option 2: Render**
- Connect GitHub repository
- Set root directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Option 3: Fly.io**
```bash
# Install Fly CLI
cd backend
flyctl launch
flyctl deploy
```

### Environment Variables

**Backend (.env):**
```env
SEC_USER_AGENT="Your Name your.email@example.com"
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## 📖 Usage Examples

### Web Interface
1. Navigate to http://localhost:3000
2. Enter ticker symbols (comma-separated): `NVDA, AAPL, TSLA`
3. Click "Start" to analyze
4. View results in table
5. Click "View Analysis" for detailed metrics
6. Results persist across page refreshes

### API Endpoints

**Analyze Company**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA"}'
```

**Response:**
```json
{
  "ticker": "NVDA",
  "cik": "0001045810",
  "score": 13.80,
  "grade": "A",
  "risk_level": "VERY LOW RISK",
  "recommendation": "STRONG BUY",
  "metrics": { ... },
  "financials": { ... }
}
```

## ⚠️ Known Limitations

### SEC API Data Quality
- **Stale Data**: Company Facts API may contain 5-15 year old data
- **Data Verification**: Always cross-reference with official 10-K filings
- **Use Case**: Best for screening and comparative analysis, not final investment decisions

### Excluded Company Types
The system automatically detects and excludes:
- Banks & financial institutions (different balance sheet structure)
- Insurance companies
- REITs (Real Estate Investment Trusts)
- Investment companies

### Analysis Constraints
- **Historical Only**: Based on past 10-K filings, not current market conditions
- **No Qualitative Factors**: Doesn't account for management quality, brand value, or industry disruption
- **Uniform Thresholds**: Same scoring applied across all industries (some variation is natural)

## 🤝 Contributing

We welcome contributions! This is an open-source project under the MIT license.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Add features or fix bugs
   - Write/update tests if applicable
   - Update documentation
4. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines
- Follow existing code style and conventions
- Test your changes locally (both frontend and backend)
- Update README/docs for new features
- Keep commits atomic and well-described

### Ideas for Contributions
- 📊 Additional financial metrics or models
- 🎨 UI/UX improvements
- 📱 Mobile app version
- 📈 Data visualization enhancements
- 🔍 Better XBRL tag coverage
- 🌍 International market support
- 📄 Export features (PDF, CSV, Excel)
- 🔔 Watchlist and alerts
- 📊 Company comparison views

## � License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### What This Means
✅ Commercial use  
✅ Modification  
✅ Distribution  
✅ Private use  
❌ Liability  
❌ Warranty  

## ⚖️ Disclaimer

**IMPORTANT**: This tool is provided for educational and informational purposes only. It should **NOT** be construed as investment advice.

- Always conduct your own due diligence
- Consult with qualified financial professionals
- Verify all data with official SEC filings
- Past performance does not guarantee future results
- The scores are algorithmic assessments and may not accurately predict future performance or bankruptcy risk

## 🙏 Acknowledgments

- **SEC EDGAR**: Data provided by the U.S. Securities and Exchange Commission
- **shadcn/ui**: Beautiful UI components
- **Vercel**: Hosting and deployment platform
- **FastAPI**: Modern Python web framework
- **Next.js**: React framework for production

## 📬 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/rp0201/10k-distress-longevity-analysis/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rp0201/10k-distress-longevity-analysis/discussions)
- **Documentation**: See `backend/README.md` and `frontend/README.md`

## 🗺️ Roadmap

### Planned Features
- [ ] Historical score tracking and trends
- [ ] Peer comparison analysis
- [ ] Industry-specific scoring adjustments
- [ ] Automated watchlist monitoring
- [ ] Email/SMS alerts for score changes
- [ ] Export to PDF/Excel
- [ ] API rate limiting and authentication
- [ ] Batch upload via CSV
- [ ] Interactive charts and visualizations
- [ ] Machine learning model improvements

### In Progress
- [x] Basic web interface
- [x] Multi-company analysis
- [x] Data persistence
- [x] Mobile responsiveness
- [x] Deployment configuration

---

Made with ❤️ for the open source community

**Star ⭐ this repo if you find it useful!**
