'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { signals } from '@/lib/api';

function SignalBadge({ direction }: { direction: string }) {
  const config: Record<string, { label: string; icon: string; class: string }> = {
    strong_bullish: { label: 'Strong Bullish', icon: '▲▲', class: 'signal-strong-bullish' },
    bullish: { label: 'Bullish', icon: '▲', class: 'signal-bullish' },
    neutral: { label: 'Neutral', icon: '◆', class: 'signal-neutral' },
    bearish: { label: 'Bearish', icon: '▼', class: 'signal-bearish' },
    strong_bearish: { label: 'Strong Bearish', icon: '▼▼', class: 'signal-strong-bearish' },
  };
  const c = config[direction] || config.neutral;
  return <span className={`signal-badge ${c.class}`}>{c.icon} {c.label}</span>;
}

export default function SignalCenterPage() {
  const [signalData, setSignalData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>('all');
  const [assetTypeFilter, setAssetTypeFilter] = useState<string>('all');

  useEffect(() => {
    async function fetchSignals() {
      try {
        setLoading(true);
        const params: Record<string, string> = { limit: '50' };
        if (filter !== 'all') params.direction = filter;
        if (assetTypeFilter !== 'all') params.asset_type = assetTypeFilter;

        const result: any = await signals.list(params);
        setSignalData(result?.items || []);
        setError(null);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchSignals();
  }, [filter, assetTypeFilter]);

  return (
    <div className="min-h-screen p-4 md:p-6">
      <Link href="/" className="text-[var(--text-accent)] text-sm mb-4 block no-underline hover:underline">← Dashboard</Link>

      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">📡 Signal Center</h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">Evidence-based analytical signals • Not investment advice</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-6">
        <div className="flex gap-1 bg-[var(--bg-secondary)] rounded-lg p-1">
          {['all', 'strong_bullish', 'bullish', 'neutral', 'bearish', 'strong_bearish'].map((d) => (
            <button
              key={d}
              onClick={() => setFilter(d)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium border-none cursor-pointer transition-colors ${
                filter === d ? 'bg-[var(--bg-tertiary)] text-[var(--text-accent)]' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              {d === 'all' ? 'All' : d.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </button>
          ))}
        </div>
        <div className="flex gap-1 bg-[var(--bg-secondary)] rounded-lg p-1">
          {['all', 'stock', 'crypto'].map((t) => (
            <button
              key={t}
              onClick={() => setAssetTypeFilter(t)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium border-none cursor-pointer transition-colors ${
                assetTypeFilter === t ? 'bg-[var(--bg-tertiary)] text-[var(--text-accent)]' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              {t === 'all' ? 'All Assets' : t === 'stock' ? '📈 Stocks' : '₿ Crypto'}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="card mb-4" style={{ background: 'var(--bearish-bg)' }}>
          <p className="text-[var(--bearish)] text-sm">Error: {error}</p>
        </div>
      )}

      {loading ? (
        <div className="space-y-3">
          {[...Array(6)].map((_, i) => <div key={i} className="skeleton h-24 rounded-xl" />)}
        </div>
      ) : (
        <div className="space-y-4">
          {signalData.length === 0 ? (
            <div className="card text-center py-8">
              <p className="text-[var(--text-muted)]">No signals match the current filters.</p>
            </div>
          ) : (
            signalData.map((sig: any, i: number) => (
              <Link
                key={i}
                href={`/asset/${sig.symbol}`}
                className="card block no-underline hover:border-[var(--border-accent)] transition-all"
              >
                <div className="flex flex-col md:flex-row md:items-center gap-4">
                  {/* Left: Asset Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-lg font-bold text-[var(--text-primary)]">{sig.symbol}</span>
                      <span className="text-sm text-[var(--text-secondary)]">{sig.asset_name}</span>
                      <SignalBadge direction={sig.direction} />
                    </div>
                    <div className="flex flex-wrap gap-4 text-xs text-[var(--text-muted)]">
                      <span>Score: <span className="mono font-medium text-[var(--text-primary)]">{sig.final_score?.toFixed(1)}</span></span>
                      <span>Confidence: <span className="mono font-medium text-[var(--text-primary)]">{sig.confidence_score?.toFixed(0)}%</span></span>
                      <span>Risk: <span className="capitalize">{sig.risk_level?.replace('_', ' ')}</span></span>
                      <span>Horizon: <span className="capitalize">{sig.time_horizon?.replace('_', ' ')}</span></span>
                      <span>Range: <span className="mono">{sig.expected_move_low}% to {sig.expected_move_high}%</span></span>
                    </div>
                  </div>

                  {/* Right: Price */}
                  <div className="text-right">
                    <div className="text-lg font-bold mono text-[var(--text-primary)]">${sig.price_at_signal?.toFixed(2)}</div>
                  </div>
                </div>

                {/* Factors Row */}
                <div className="flex flex-wrap gap-2 mt-3">
                  {sig.bull_factors?.slice(0, 2).map((f: any, j: number) => (
                    <span key={`b${j}`} className="text-[0.6875rem] px-2 py-0.5 rounded" style={{ background: 'var(--bullish-bg)', color: 'var(--bullish)' }}>
                      ▲ {f.factor?.substring(0, 60)}{f.factor?.length > 60 ? '...' : ''}
                    </span>
                  ))}
                  {sig.bear_factors?.slice(0, 2).map((f: any, j: number) => (
                    <span key={`r${j}`} className="text-[0.6875rem] px-2 py-0.5 rounded" style={{ background: 'var(--bearish-bg)', color: 'var(--bearish)' }}>
                      ▼ {f.factor?.substring(0, 60)}{f.factor?.length > 60 ? '...' : ''}
                    </span>
                  ))}
                </div>
              </Link>
            ))
          )}
        </div>
      )}

      <div className="disclaimer-box mt-6">
        <strong>⚠️ Disclaimer:</strong> All signals are analytical and probabilistic. They do not constitute personalized investment advice and do not guarantee future performance. Users remain fully responsible for their own investment decisions.
      </div>
    </div>
  );
}
