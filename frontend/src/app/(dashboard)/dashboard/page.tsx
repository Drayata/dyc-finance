'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { markets, news, signals } from '@/lib/api';
import type { MarketOverview, NewsArticle, Signal } from '@/types';

// === Helper Components ===

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

function FormatNumber({ value, prefix = '', suffix = '', decimals = 2 }: {
  value?: number | null; prefix?: string; suffix?: string; decimals?: number;
}) {
  if (value == null) return <span className="text-[var(--text-muted)]">—</span>;
  const formatted = new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
  return <span className="mono">{prefix}{formatted}{suffix}</span>;
}

function PriceChange({ value }: { value?: number | null }) {
  if (value == null) return <span className="text-[var(--text-muted)]">—</span>;
  const color = value > 0 ? 'var(--bullish)' : value < 0 ? 'var(--bearish)' : 'var(--text-muted)';
  const icon = value > 0 ? '▲' : value < 0 ? '▼' : '—';
  return (
    <span className="mono" style={{ color }}>
      {icon} {Math.abs(value).toFixed(2)}%
    </span>
  );
}

function SkeletonCard() {
  return <div className="card"><div className="skeleton h-4 w-3/4 mb-3" /><div className="skeleton h-8 w-1/2 mb-2" /><div className="skeleton h-3 w-full" /></div>;
}

function DisclaimerBar() {
  return (
    <div className="disclaimer-box mt-4">
      <strong>⚠️ Disclaimer:</strong> The information provided is for educational and market-analysis purposes only.
      All signals are probabilistic and do not guarantee future performance. This does not constitute personalized investment advice.
    </div>
  );
}

// === Main Dashboard Page ===

export default function DashboardPage() {
  const [overview, setOverview] = useState<any>(null);
  const [newsData, setNewsData] = useState<any[]>([]);
  const [signalData, setSignalData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>('');

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const [overviewRes, newsRes, signalRes] = await Promise.all([
          markets.overview().catch(() => null),
          news.highImpact(5).catch(() => ({ items: [] })),
          signals.list({ limit: 10 }).catch(() => ({ items: [] })),
        ]);

        setOverview(overviewRes);
        setNewsData((newsRes as any)?.items || []);
        setSignalData((signalRes as any)?.items || []);
        setLastUpdated(new Date().toLocaleTimeString());
        setError(null);
      } catch (err: any) {
        setError(err.message || 'Failed to load data. Is the backend running?');
      } finally {
        setLoading(false);
      }
    }
    fetchData();
    const interval = setInterval(fetchData, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen p-4 md:p-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">Market Dashboard</h1>
            <p className="text-sm text-[var(--text-secondary)] mt-1">
              Real-time market overview • {lastUpdated && `Last updated: ${lastUpdated}`}
            </p>
          </div>
          <div className="flex items-center gap-2 mt-3 md:mt-0">
            <span className="text-xs px-2 py-1 rounded-full bg-[var(--warning-bg)] text-[var(--warning)]">Demo Mode</span>
            <span className="text-xs text-[var(--text-muted)]">{overview?.market_regime || '—'}</span>
          </div>
        </div>

        {error && (
          <div className="card mb-6 border-[var(--bearish-border)]" style={{ background: 'var(--bearish-bg)' }}>
            <p className="text-[var(--bearish)] text-sm">
              <strong>⚠️ Connection Error:</strong> {error}
            </p>
            <p className="text-xs text-[var(--text-muted)] mt-1">
              Make sure the backend is running at {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
            </p>
          </div>
        )}

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            {[...Array(4)].map((_, i) => <SkeletonCard key={i} />)}
          </div>
        ) : (
          <>
            {/* Market Indices */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              {overview?.global_market?.indices?.map((idx: any) => (
                <div key={idx.symbol} className="card">
                  <div className="text-xs text-[var(--text-muted)] mb-1">{idx.country}</div>
                  <div className="text-sm font-medium text-[var(--text-primary)] truncate">{idx.name}</div>
                  <div className="flex items-end justify-between mt-2">
                    <div className="text-xl font-bold mono text-[var(--text-primary)]">
                      <FormatNumber value={idx.price} />
                    </div>
                    <PriceChange value={idx.change_pct} />
                  </div>
                </div>
              ))}
            </div>

            {/* Crypto Market Summary */}
            {overview?.crypto_market && (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                <div className="card">
                  <div className="text-xs text-[var(--text-muted)]">Crypto Market Cap</div>
                  <div className="text-lg font-bold mono text-[var(--text-primary)] mt-1">
                    ${((overview.crypto_market.total_market_cap || 0) / 1e12).toFixed(2)}T
                  </div>
                </div>
                <div className="card">
                  <div className="text-xs text-[var(--text-muted)]">BTC Dominance</div>
                  <div className="text-lg font-bold mono text-[var(--text-primary)] mt-1">
                    {overview.crypto_market.btc_dominance}%
                  </div>
                </div>
                <div className="card">
                  <div className="text-xs text-[var(--text-muted)]">ETH Dominance</div>
                  <div className="text-lg font-bold mono text-[var(--text-primary)] mt-1">
                    {overview.crypto_market.eth_dominance}%
                  </div>
                </div>
                <div className="card">
                  <div className="text-xs text-[var(--text-muted)]">Fear & Greed</div>
                  <div className="text-lg font-bold mono mt-1" style={{
                    color: (overview.crypto_market.fear_greed_index || 50) > 60 ? 'var(--bullish)' :
                           (overview.crypto_market.fear_greed_index || 50) < 40 ? 'var(--bearish)' : 'var(--text-primary)'
                  }}>
                    {overview.crypto_market.fear_greed_index} — {overview.crypto_market.fear_greed_label}
                  </div>
                </div>
              </div>
            )}

            {/* Two Column Layout: Signals + News */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              {/* Top Signals */}
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-base font-semibold text-[var(--text-primary)]">📡 Active Signals</h2>
                  <Link href="/signals" className="text-xs text-[var(--text-accent)] no-underline hover:underline">View All →</Link>
                </div>
                <div className="space-y-3">
                  {signalData.length === 0 ? (
                    <p className="text-sm text-[var(--text-muted)] text-center py-4">No signals available. Start the backend to generate signals.</p>
                  ) : (
                    signalData.slice(0, 6).map((sig: any, i: number) => (
                      <Link
                        key={i}
                        href={`/asset/${sig.symbol}`}
                        className="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-[var(--bg-tertiary)] no-underline transition-colors"
                      >
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-semibold text-[var(--text-primary)]">{sig.symbol}</span>
                            <span className="text-xs text-[var(--text-muted)] truncate">{sig.asset_name}</span>
                          </div>
                          <div className="flex items-center gap-2 mt-1">
                            <span className="text-xs text-[var(--text-muted)]">Conf: {sig.confidence_score?.toFixed(0)}%</span>
                            <span className="text-xs text-[var(--text-muted)]">•</span>
                            <span className="text-xs text-[var(--text-muted)]">{sig.time_horizon?.replace('_', ' ')}</span>
                          </div>
                        </div>
                        <SignalBadge direction={sig.direction} />
                      </Link>
                    ))
                  )}
                </div>
              </div>

              {/* High-Impact News */}
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-base font-semibold text-[var(--text-primary)]">📰 High-Impact News</h2>
                  <Link href="/news" className="text-xs text-[var(--text-accent)] no-underline hover:underline">View All →</Link>
                </div>
                <div className="space-y-3">
                  {newsData.length === 0 ? (
                    <p className="text-sm text-[var(--text-muted)] text-center py-4">No news available. Start the backend to fetch news.</p>
                  ) : (
                    newsData.slice(0, 5).map((article: any, i: number) => (
                      <div key={i} className="py-2 px-3 rounded-lg hover:bg-[var(--bg-tertiary)] transition-colors cursor-pointer">
                        <div className="flex items-start gap-2">
                          <div className="flex-1 min-w-0">
                            <div className="text-sm text-[var(--text-primary)] font-medium leading-tight">{article.title}</div>
                            <div className="flex items-center gap-2 mt-1.5">
                              <span className="text-xs text-[var(--text-muted)]">{article.source_name}</span>
                              {article.is_verified === false && (
                                <span className="text-xs px-1.5 py-0.5 rounded bg-[var(--warning-bg)] text-[var(--warning)]">⚠ Unverified</span>
                              )}
                              <span className="text-xs text-[var(--text-muted)]">Impact: {article.impact_score}</span>
                              {article.impact_direction && (
                                <span className={`text-xs ${
                                  article.impact_direction === 'bullish' ? 'text-[var(--bullish)]' :
                                  article.impact_direction === 'bearish' ? 'text-[var(--bearish)]' :
                                  'text-[var(--text-muted)]'
                                }`}>
                                  {article.impact_direction}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>

            {/* Movers */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              {/* Top Gainers */}
              <div className="card">
                <h2 className="text-base font-semibold text-[var(--text-primary)] mb-3">🟢 Top Gainers</h2>
                <div className="table-responsive">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-xs text-[var(--text-muted)] border-b border-[var(--border-primary)]">
                        <th className="text-left py-2 font-medium">Asset</th>
                        <th className="text-right py-2 font-medium">Price</th>
                        <th className="text-right py-2 font-medium">Change</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(overview?.top_gainers || []).slice(0, 5).map((g: any, i: number) => (
                        <tr key={i} className="border-b border-[var(--border-primary)] last:border-0 hover:bg-[var(--bg-tertiary)]">
                          <td className="py-2">
                            <Link href={`/asset/${g.symbol}`} className="text-[var(--text-primary)] no-underline hover:text-[var(--text-accent)] font-medium">
                              {g.symbol}
                            </Link>
                          </td>
                          <td className="text-right mono"><FormatNumber value={g.price} /></td>
                          <td className="text-right"><PriceChange value={g.change_pct} /></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Top Losers */}
              <div className="card">
                <h2 className="text-base font-semibold text-[var(--text-primary)] mb-3">🔴 Top Losers</h2>
                <div className="table-responsive">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-xs text-[var(--text-muted)] border-b border-[var(--border-primary)]">
                        <th className="text-left py-2 font-medium">Asset</th>
                        <th className="text-right py-2 font-medium">Price</th>
                        <th className="text-right py-2 font-medium">Change</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(overview?.top_losers || []).slice(0, 5).map((l: any, i: number) => (
                        <tr key={i} className="border-b border-[var(--border-primary)] last:border-0 hover:bg-[var(--bg-tertiary)]">
                          <td className="py-2">
                            <Link href={`/asset/${l.symbol}`} className="text-[var(--text-primary)] no-underline hover:text-[var(--text-accent)] font-medium">
                              {l.symbol}
                            </Link>
                          </td>
                          <td className="text-right mono"><FormatNumber value={l.price} /></td>
                          <td className="text-right"><PriceChange value={l.change_pct} /></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <DisclaimerBar />
          </>
        )}
    </div>
  );
}
