# Frontend - 10-K Financial Distress Analysis

Modern web interface for analyzing financial distress using SEC 10-K filings. Built with Next.js, TypeScript, and Tailwind CSS.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Set up environment variables (see below)
cp .env.example .env.local

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Tech Stack

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **UI Components**: shadcn/ui
- **Icons**: Lucide React
- **State Management**: React hooks + localStorage persistence
- **Deployment**: Vercel

## Features

- ✅ **Multi-ticker Analysis**: Analyze multiple companies simultaneously
- ✅ **Persistent Data**: Local storage saves your analyses across sessions
- ✅ **Responsive Design**: Mobile-friendly interface with adaptive layouts
- ✅ **Data Quality Warnings**: Alerts for stale or outdated SEC data
- ✅ **Sticky Table Headers**: Easy navigation through large result sets

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout with metadata
│   ├── page.tsx                # Home page with analysis interface
│   ├── limitations/
│   │   └── page.tsx            # Limitations & disclaimer page
│   └── globals.css             # Global styles
├── components/
│   ├── site-header.tsx         # Navigation header
│   ├── output-table.tsx        # Results table with analysis
│   └── ui/                     # shadcn/ui components
├── lib/
│   └── utils.ts                # Utility functions
├── public/
│   ├── 10k_analyzer.svg        # Logo
│   ├── empty_state.svg         # Empty state illustration
│   └── github.svg              # GitHub icon
└── package.json
```

## Environment Variables

Create a `.env.local` file:

```env
# Backend API URL (required)
NEXT_PUBLIC_API_URL=http://localhost:8000

# For production deployment
# NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

## Integration with Backend

The frontend communicates with the FastAPI backend via REST API:

**Development:**
```bash
# Terminal 1: Start backend
cd ../backend
fastapi dev main.py

# Terminal 2: Start frontend
cd frontend
npm run dev
```

**Production:**
- Frontend: Deploy to Vercel (automatic from GitHub)
- Backend: Deploy FastAPI to Railway/Render/Fly.io
- Update `NEXT_PUBLIC_API_URL` environment variable in Vercel

## Deployment to Vercel

### Automatic Deployment (Recommended)

1. Push your code to GitHub
2. Import your repository to [Vercel](https://vercel.com)
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL
4. Deploy!

### Manual Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Vercel Configuration

The project is configured for optimal Vercel deployment:
- ✅ Next.js 15+ App Router
- ✅ Automatic static optimization
- ✅ Edge runtime compatible
- ✅ Environment variables support

## Key Components

### `app/page.tsx`
- Main analysis interface
- Ticker input and submission
- Results table with sticky headers
- localStorage persistence
- Error handling with alerts

### `components/output-table.tsx`
- Input form integration
- Company analysis table
- Comprehensive analysis modal
- Empty state handling
- Clear all functionality

### `components/site-header.tsx`
- Responsive navigation
- Desktop: NavigationMenu component
- Mobile: Sheet drawer menu
- GitHub repository link

### `app/limitations/page.tsx`
- SEC API constraints documentation
- Company type restrictions
- Analytical limitations
- Legal disclaimer

## Component Library

This project uses [shadcn/ui](https://ui.shadcn.com/) components:

```bash
# Add new components
npx shadcn@latest add [component-name]

# Example: Add card component
npx shadcn@latest add card
```

**Currently used components:**
- Alert
- Button
- Dialog
- Input
- Navigation Menu
- Sheet
- Sonner (Toast)
- Table

## Development Tips

### Adding a New Page
```typescript
// app/new-page/page.tsx
export default function NewPage() {
  return <div>New Page Content</div>
}
```

### Styling Guidelines
- Use Tailwind CSS utility classes
- Follow existing color scheme: `bg-[#12100E]`, `border-[#31302F]`
- Maintain consistent spacing with existing components
- Use responsive breakpoints: `sm:`, `md:`, `lg:`, `xl:`

### State Management
- Use React hooks (`useState`, `useEffect`)
- Persist important data to localStorage
- Clear localStorage on logout/clear actions

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Optimizations

- ✅ Next.js automatic code splitting
- ✅ Image optimization with Next.js Image
- ✅ Static asset optimization
- ✅ Lazy loading for modal content
- ✅ Efficient re-renders with React hooks

## Contributing

This is an open-source project! Contributions are welcome.

### Getting Started
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Workflow
1. Run backend: `cd backend && fastapi dev main.py`
2. Run frontend: `cd frontend && npm run dev`
3. Make changes and test locally
4. Ensure no TypeScript errors: `npm run build`
5. Submit PR with description

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
npm run dev -- -p 3001
```

### API Connection Issues
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Ensure CORS is configured in backend

### Build Errors
```bash
# Clear cache and rebuild
rm -rf .next
npm run build
```

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is for educational and informational purposes only. It should not be construed as investment advice. Always conduct your own due diligence and consult with qualified financial professionals before making investment decisions.

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Vercel Deployment](https://vercel.com/docs)
