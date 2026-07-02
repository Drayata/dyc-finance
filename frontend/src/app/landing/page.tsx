'use client';

import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[var(--bg-primary)]">
      {/* Navigation */}
      <nav className="flex items-center justify-between px-6 py-4 border-b border-[var(--border-primary)] bg-[var(--bg-secondary)]">
        <Link href="/" className="flex items-center gap-3 no-underline">
          <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl" style={{ background: 'var(--gradient-primary)' }}>
            🧠
          </div>
          <div>
            <div className="text-lg font-bold text-[var(--text-primary)] leading-tight">MarketPulse</div>
            <div className="text-xs text-[var(--text-accent)] font-medium">AI Intelligence</div>
          </div>
        </Link>
        <div className="flex items-center gap-4">
          <Link href="/login" className="text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors no-underline">
            Log in
          </Link>
          <Link href="/register" className="text-sm font-medium px-4 py-2 bg-[var(--text-accent)] text-white rounded-lg hover:opacity-90 transition-opacity no-underline">
            Sign up
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-6 py-20 md:py-32 text-center max-w-5xl mx-auto">
        <h1 className="text-4xl md:text-6xl font-bold text-[var(--text-primary)] mb-6 tracking-tight leading-tight">
          Evidence-Based Market Intelligence <br className="hidden md:block" />
          <span className="text-transparent bg-clip-text" style={{ backgroundImage: 'var(--gradient-primary)' }}>
            Powered by AI
          </span>
        </h1>
        <p className="text-lg md:text-xl text-[var(--text-secondary)] mb-10 max-w-2xl mx-auto leading-relaxed">
          Monitor stocks and cryptocurrencies, identify market-moving news, and analyze potential impact with transparent, multi-factor AI models.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/register" className="w-full sm:w-auto px-8 py-3.5 bg-[var(--text-accent)] text-white rounded-xl font-medium hover:opacity-90 transition-opacity text-lg no-underline shadow-lg shadow-blue-500/20">
            Start Exploring
          </Link>
          <Link href="#features" className="w-full sm:w-auto px-8 py-3.5 bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] rounded-xl font-medium hover:bg-[var(--bg-tertiary)] transition-colors text-lg no-underline">
            Learn More
          </Link>
        </div>
        
        <div className="mt-8 text-xs text-[var(--text-muted)] flex items-center justify-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[var(--bullish)]"></span>
          Educational purposes only. Not financial advice.
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="px-6 py-20 bg-[var(--bg-secondary)] border-y border-[var(--border-primary)]">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-[var(--text-primary)] mb-4">A Professional Analysis Platform</h2>
            <p className="text-[var(--text-secondary)] max-w-2xl mx-auto">
              MarketPulse AI replaces emotion with data. Our models ingest hundreds of data points per second to provide transparent analytical signals.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="card p-8 bg-[var(--bg-primary)] hover:border-[var(--border-accent)] transition-all">
              <div className="w-12 h-12 rounded-xl bg-[var(--bg-tertiary)] flex items-center justify-center text-2xl mb-6">📰</div>
              <h3 className="text-xl font-bold text-[var(--text-primary)] mb-3">News Intelligence</h3>
              <p className="text-sm text-[var(--text-secondary)] leading-relaxed">
                Real-time ingestion of global financial news. Our NLP engine extracts entities, determines sentiment, and assesses impact pathways automatically.
              </p>
            </div>
            <div className="card p-8 bg-[var(--bg-primary)] hover:border-[var(--border-accent)] transition-all border border-[var(--border-accent)]">
              <div className="w-12 h-12 rounded-xl bg-[var(--bg-tertiary)] flex items-center justify-center text-2xl mb-6">📡</div>
              <h3 className="text-xl font-bold text-[var(--text-primary)] mb-3">Hybrid AI Signals</h3>
              <p className="text-sm text-[var(--text-secondary)] leading-relaxed">
                Combining technical indicators, fundamental ratios, on-chain metrics, and news sentiment into a single, transparent composite score.
              </p>
            </div>
            <div className="card p-8 bg-[var(--bg-primary)] hover:border-[var(--border-accent)] transition-all">
              <div className="w-12 h-12 rounded-xl bg-[var(--bg-tertiary)] flex items-center justify-center text-2xl mb-6">🔍</div>
              <h3 className="text-xl font-bold text-[var(--text-primary)] mb-3">Transparent Logic</h3>
              <p className="text-sm text-[var(--text-secondary)] leading-relaxed">
                No black boxes. Every signal includes its component weights, contributing bull/bear factors, identified risks, and invalidation conditions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Model Transparency Section */}
      <section className="px-6 py-20 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl font-bold text-[var(--text-primary)] mb-6">Designed for Education and Insight</h2>
            <div className="space-y-6">
              <div className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-[var(--bg-tertiary)] flex items-center justify-center shrink-0">1</div>
                <div>
                  <h4 className="font-bold text-[var(--text-primary)] mb-1">Multi-Market Coverage</h4>
                  <p className="text-sm text-[var(--text-secondary)]">Analyze US Equities, Indonesian Stocks, and major Cryptocurrencies in one platform.</p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-[var(--bg-tertiary)] flex items-center justify-center shrink-0">2</div>
                <div>
                  <h4 className="font-bold text-[var(--text-primary)] mb-1">Customizable Alerts</h4>
                  <p className="text-sm text-[var(--text-secondary)]">Set rule-based alerts for price movements, technical crossovers, or news sentiment shifts.</p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-[var(--bg-tertiary)] flex items-center justify-center shrink-0">3</div>
                <div>
                  <h4 className="font-bold text-[var(--text-primary)] mb-1">Backtesting (Coming Soon)</h4>
                  <p className="text-sm text-[var(--text-secondary)]">Validate signal performance against historical data with full walk-forward methodology.</p>
                </div>
              </div>
            </div>
          </div>
          <div className="card p-6 bg-[var(--bg-secondary)] border border-[var(--border-primary)] shadow-2xl">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-4 border-b border-[var(--border-primary)] pb-2">Sample Signal Output</h3>
            <div className="space-y-3 font-mono text-xs">
              <div className="flex justify-between"><span className="text-[var(--text-muted)]">Asset:</span> <span className="text-[var(--text-primary)]">BTC/USD</span></div>
              <div className="flex justify-between"><span className="text-[var(--text-muted)]">Direction:</span> <span className="text-[var(--bullish)]">Bullish</span></div>
              <div className="flex justify-between"><span className="text-[var(--text-muted)]">Confidence:</span> <span className="text-[var(--text-primary)]">78.4%</span></div>
              <div className="flex justify-between"><span className="text-[var(--text-muted)]">Time Horizon:</span> <span className="text-[var(--text-primary)]">1-4 Weeks</span></div>
              <div className="mt-2 text-[var(--text-muted)]">Top Factors:</div>
              <div className="pl-4 text-[var(--bullish)]">+ Moving average golden cross (SMA50/200)</div>
              <div className="pl-4 text-[var(--bullish)]">+ High positive news sentiment (+0.65)</div>
              <div className="pl-4 text-[var(--bullish)]">+ Exchange outflow spike</div>
              <div className="mt-2 text-[var(--warning)] text-[0.65rem]">⚠ Invalidation: Daily close below $60,000</div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer / Disclaimer */}
      <footer className="bg-[var(--bg-secondary)] border-t border-[var(--border-primary)] py-12 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="text-xl">🧠</div>
            <span className="font-bold text-[var(--text-primary)]">MarketPulse AI</span>
          </div>
          <div className="flex gap-6 text-sm">
            <Link href="/terms" className="text-[var(--text-secondary)] hover:text-[var(--text-primary)] no-underline">Terms</Link>
            <Link href="/privacy" className="text-[var(--text-secondary)] hover:text-[var(--text-primary)] no-underline">Privacy</Link>
            <Link href="/disclaimer" className="text-[var(--text-secondary)] hover:text-[var(--text-primary)] no-underline">Disclaimer</Link>
          </div>
        </div>
        <div className="max-w-7xl mx-auto mt-8 pt-8 border-t border-[var(--border-primary)] text-xs text-[var(--text-muted)] leading-relaxed text-justify">
          <strong>IMPORTANT DISCLAIMER:</strong> MarketPulse AI is an educational technology platform and is not a registered broker, dealer, or investment adviser. 
          The content, signals, sentiment analysis, and all other information provided by the platform are generated by automated algorithms for informational and educational purposes only. 
          They do not constitute financial advice, investment recommendations, or an offer to buy or sell any securities or digital assets. 
          All trading and investment involves significant risk of loss. Users are solely responsible for their own investment decisions and should consult with a qualified, licensed financial professional before making any financial decisions. 
          Past performance of any model or strategy is not indicative of future results.
        </div>
      </footer>
    </div>
  );
}
