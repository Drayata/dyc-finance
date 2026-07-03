'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { markets } from '@/lib/api';
import CandlestickChart from '@/components/charts/CandlestickChart';
import { useUserPreferences } from '@/context/UserPreferences';

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

function ScoreBar({ value, max = 100, color = 'var(--text-accent)' }: { value: number; max?: number; color?: string }) {
  const pct = Math.abs(value) / max * 100;
  return (
    <div className="score-bar w-full">
      <div className="score-bar-fill" style={{ width: `${Math.min(pct, 100)}%`, background: color }} />
    </div>
  );
}

export default function AssetDetailPage() {
  const params = useParams();
  const symbol = params.symbol as string;
  const { viewMode } = useUserPreferences();
  const [data, setData] = useState<any>(null);
  const [candles, setCandles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'technical' | 'news' | 'signal'>('overview');

  useEffect(() => {
    async function fetchAsset() {
      try {
        setLoading(true);
        const [result, candlesResult] = await Promise.all([
          markets.getAsset(symbol),
          markets.getCandles(symbol, '1d', 100).catch(() => [])
        ]);
        setData(result);
        setCandles((candlesResult as any[]) || []);
        setError(null);
      } catch (err: any) {
        setError(err.message || 'Failed to load asset data');
      } finally {
        setLoading(false);
      }
    }
    if (symbol) fetchAsset();
  }, [symbol]);

  if (loading) {
    return (
      <div className="min-h-screen p-4 md:p-6">
        <div className="skeleton h-8 w-48 mb-4" />
        <div className="skeleton h-64 w-full mb-4" />
        <div className="grid grid-cols-2 gap-4">
          <div className="skeleton h-32" />
          <div className="skeleton h-32" />
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen p-4 md:p-6">
        <Link href="/dashboard" className="text-[var(--text-accent)] text-sm mb-4 block no-underline">← Back to Dashboard</Link>
        <div className="card" style={{ background: 'var(--bearish-bg)', borderColor: 'var(--bearish-border)' }}>
          <p className="text-[var(--bearish)]">Error: {error || 'Asset not found'}</p>
        </div>
      </div>
    );
  }

  const { asset, price, indicators, fundamentals, onchain, news: assetNews, signal } = data;

  return (
    <div className="min-h-screen p-4 md:p-6">
      {/* Breadcrumb */}
      <Link href="/dashboard" className="text-[var(--text-accent)] text-sm mb-4 block no-underline hover:underline">← Dashboard</Link>

      {/* Asset Header */}
      <div className="card mb-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-[var(--text-primary)]">{asset.symbol}</h1>
              <span className="text-xs px-2 py-1 rounded-full bg-[var(--bg-tertiary)] text-[var(--text-muted)]">{asset.asset_type}</span>
              {data.demo_mode && <span className="text-xs px-2 py-1 rounded-full bg-[var(--warning-bg)] text-[var(--warning)]">Demo</span>}
            </div>
            <p className="text-sm text-[var(--text-secondary)] mt-1">{asset.name}</p>
            {asset.sector && <p className="text-xs text-[var(--text-muted)]">{asset.sector} • {asset.industry} • {asset.country}</p>}
          </div>

          {price && (
            <div className="text-right">
              <div className="text-3xl font-bold mono text-[var(--text-primary)]">
                {price.currency === 'IDR' ? 'Rp' : '$'}{Number(price.price).toLocaleString(undefined, { maximumFractionDigits: 8 })}
              </div>
              <div className="mt-1">
                <span className={`mono text-lg font-semibold ${(price.price_change_pct_24h || 0) >= 0 ? 'text-[var(--bullish)]' : 'text-[var(--bearish)]'}`}>
                  {(price.price_change_pct_24h || 0) >= 0 ? '▲' : '▼'} {Math.abs(price.price_change_pct_24h || 0).toFixed(2)}%
                </span>
              </div>
              <div className="text-xs text-[var(--text-muted)] mt-1">
                {price.data_freshness} • {new Date(price.data_timestamp).toLocaleTimeString()}
              </div>
            </div>
          )}
        </div>

        {/* Warnings */}
        {asset.manipulation_risk && (
          <div className="mt-3 px-3 py-2 rounded-lg text-xs font-medium" style={{ background: 'var(--bearish-bg)', color: 'var(--bearish)' }}>
            ⚠️ High Manipulation Risk — Signals may be unreliable
          </div>
        )}
        {asset.low_liquidity_warning && (
          <div className="mt-2 px-3 py-2 rounded-lg text-xs font-medium" style={{ background: 'var(--warning-bg)', color: 'var(--warning)' }}>
            ⚠️ Low Liquidity — Trade with caution
          </div>
        )}
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-1 mb-6 overflow-x-auto">
        {(['overview', 'technical', 'news', 'signal'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-lg text-sm font-medium border-none cursor-pointer whitespace-nowrap transition-colors ${
              activeTab === tab
                ? 'bg-[var(--bg-tertiary)] text-[var(--text-accent)]'
                : 'bg-transparent text-[var(--text-secondary)] hover:bg-[var(--bg-tertiary)]'
            }`}
          >
            {tab === 'overview' ? '📊 Overview' : tab === 'technical' ? '📈 Technical' : tab === 'news' ? '📰 News' : '📡 Signal'}
          </button>
        ))}
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Chart Section */}
          <div className="card h-[400px]">
            {candles.length > 0 ? (
              <CandlestickChart data={candles} height={360} />
            ) : (
              <div className="flex items-center justify-center h-full text-[var(--text-muted)]">
                No chart data available
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Price Data */}
            <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Price Data</h3>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div><span className="text-[var(--text-muted)]">Open</span><div className="mono">{price?.open_24h ? `$${Number(price.open_24h).toLocaleString()}` : '—'}</div></div>
              <div><span className="text-[var(--text-muted)]">Close</span><div className="mono">${Number(price?.price || 0).toLocaleString()}</div></div>
              <div><span className="text-[var(--text-muted)]">24h High</span><div className="mono">{price?.high_24h ? `$${Number(price.high_24h).toLocaleString()}` : '—'}</div></div>
              <div><span className="text-[var(--text-muted)]">24h Low</span><div className="mono">{price?.low_24h ? `$${Number(price.low_24h).toLocaleString()}` : '—'}</div></div>
              <div><span className="text-[var(--text-muted)]">Volume 24h</span><div className="mono">${((price?.volume_24h || 0) / 1e6).toFixed(2)}M</div></div>
              <div><span className="text-[var(--text-muted)]">Market Cap</span><div className="mono">${((price?.market_cap || 0) / 1e9).toFixed(2)}B</div></div>
            </div>
          </div>

          {/* Signal Summary */}
          {signal && (
            <div className="card">
              <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Current Signal</h3>
              <div className="flex items-center gap-3 mb-4">
                <SignalBadge direction={signal.direction} />
                <span className="text-xs text-[var(--text-muted)]">Score: {signal.final_score?.toFixed(1)}</span>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div><span className="text-[var(--text-muted)]">Confidence</span><div className="mono">{signal.confidence_score?.toFixed(1)}%</div></div>
                <div><span className="text-[var(--text-muted)]">Risk</span><div className="capitalize">{signal.risk_level?.replace('_', ' ')}</div></div>
                <div><span className="text-[var(--text-muted)]">Time Horizon</span><div className="capitalize">{signal.time_horizon?.replace('_', ' ')}</div></div>
                <div><span className="text-[var(--text-muted)]">Expected Range</span><div className="mono">{signal.expected_move_low}% to {signal.expected_move_high}%</div></div>
              </div>
              {/* Factors */}
              <div className="mt-4 space-y-2">
                {signal.bull_factors?.map((f: any, i: number) => (
                  <div key={i} className="text-xs px-2 py-1.5 rounded" style={{ background: 'var(--bullish-bg)', color: 'var(--bullish)' }}>
                    ▲ {f.factor} <span className="text-[var(--text-muted)]">({f.type})</span>
                  </div>
                ))}
                {signal.bear_factors?.map((f: any, i: number) => (
                  <div key={i} className="text-xs px-2 py-1.5 rounded" style={{ background: 'var(--bearish-bg)', color: 'var(--bearish)' }}>
                    ▼ {f.factor} <span className="text-[var(--text-muted)]">({f.type})</span>
                  </div>
                ))}
              </div>
              {/* Invalidation */}
              {signal.invalidation_conditions && (
                <div className="mt-3">
                  <div className="text-xs font-medium text-[var(--text-muted)] mb-1">Invalidation Conditions:</div>
                  {signal.invalidation_conditions.map((c: any, i: number) => (
                    <div key={i} className="text-xs text-[var(--warning)] ml-2">• {c.condition}</div>
                  ))}
                </div>
              )}
              <div className="mt-3 text-[0.625rem] text-[var(--text-muted)]">{signal.disclaimer}</div>
            </div>
          )}


            {/* Fundamentals (Advanced Only) */}
            {viewMode === 'advanced' && fundamentals && (
              <div className="card">
                <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Fundamentals</h3>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div><span className="text-[var(--text-muted)]">P/E Ratio</span><div className="mono">{fundamentals.pe_ratio?.toFixed(2) || '—'}</div></div>
                  <div><span className="text-[var(--text-muted)]">P/B Ratio</span><div className="mono">{fundamentals.pb_ratio?.toFixed(2) || '—'}</div></div>
                  <div><span className="text-[var(--text-muted)]">Div Yield</span><div className="mono">{(fundamentals.dividend_yield * 100).toFixed(2)}%</div></div>
                  <div><span className="text-[var(--text-muted)]">EPS</span><div className="mono">${fundamentals.eps?.toFixed(2) || '—'}</div></div>
                </div>
              </div>
            )}
            
            {/* Simple Mode Info */}
            {viewMode === 'simple' && (
              <div className="card bg-[var(--bg-secondary)] border border-[var(--border-primary)]">
                <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-2">Market Pulse AI Analysis</h3>
                <p className="text-sm text-[var(--text-secondary)]">
                  Based on current market conditions, {asset.symbol} is showing a {signal?.direction.replace('_', ' ')} trend. 
                  This signal is generated using a combination of technical indicators and sentiment analysis.
                </p>
                <button onClick={() => window.location.href='/settings'} className="mt-3 text-xs text-[var(--text-accent)] hover:underline bg-transparent border-none cursor-pointer p-0">
                  Enable Advanced Mode for more details
                </button>
              </div>
            )}
          </div>
        </div>
      )}



          {/* On-Chain (Crypto only) */}
          {onchain && (
            <div className="card">
              <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">On-Chain Metrics</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div><span className="text-[var(--text-muted)]">Active Addresses</span><div className="mono">{(onchain.active_addresses || 0).toLocaleString()}</div></div>
                <div><span className="text-[var(--text-muted)]">Tx Count</span><div className="mono">{(onchain.transaction_count || 0).toLocaleString()}</div></div>
                <div><span className="text-[var(--text-muted)]">TVL</span><div className="mono">${((onchain.tvl || 0) / 1e9).toFixed(2)}B</div></div>
                <div><span className="text-[var(--text-muted)]">Staking Ratio</span><div className="mono">{((onchain.staking_ratio || 0) * 100).toFixed(1)}%</div></div>
                <div><span className="text-[var(--text-muted)]">Exchange Inflow</span><div className="mono">{(onchain.exchange_inflow || 0).toLocaleString()}</div></div>
                <div><span className="text-[var(--text-muted)]">Whale Txs</span><div className="mono">{onchain.whale_transactions}</div></div>
              </div>
              <div className="text-xs text-[var(--text-muted)] mt-3">Provider: {onchain.provider} • {onchain.data_freshness || 'demo'}</div>
            </div>
          )}


      {/* Technical Tab */}
      {activeTab === 'technical' && (
        <div className="space-y-6">
          {viewMode === 'simple' ? (
            <div className="card text-center p-8">
              <h3 className="text-lg font-medium text-[var(--text-primary)] mb-2">Advanced Technicals Hidden</h3>
              <p className="text-[var(--text-secondary)] mb-4">Technical indicators and raw model data are hidden in Simple Mode.</p>
              <Link href="/settings" className="px-4 py-2 rounded-lg bg-[var(--text-accent)] text-white text-sm no-underline hover:opacity-90 inline-block">
                Enable Advanced Mode
              </Link>
            </div>
          ) : indicators && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Moving Averages</h3>
            <div className="space-y-2 text-sm">
              {[['SMA 20', indicators.sma_20], ['SMA 50', indicators.sma_50], ['SMA 200', indicators.sma_200], ['EMA 12', indicators.ema_12], ['EMA 26', indicators.ema_26]].map(([label, val]: any) => (
                <div key={label} className="flex justify-between">
                  <span className="text-[var(--text-muted)]">{label}</span>
                  <span className="mono">{val != null ? Number(val).toFixed(4) : '—'}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Oscillators</h3>
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-[var(--text-muted)]">RSI (14)</span>
                  <span className={`mono ${(indicators.rsi_14 || 50) > 70 ? 'text-[var(--bearish)]' : (indicators.rsi_14 || 50) < 30 ? 'text-[var(--bullish)]' : ''}`}>
                    {indicators.rsi_14?.toFixed(1) || '—'}
                  </span>
                </div>
                <ScoreBar value={indicators.rsi_14 || 0} color={
                  (indicators.rsi_14 || 50) > 70 ? 'var(--bearish)' : (indicators.rsi_14 || 50) < 30 ? 'var(--bullish)' : 'var(--text-accent)'
                } />
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-[var(--text-muted)]">MACD</span>
                <span className="mono">{indicators.macd?.toFixed(4) || '—'}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-[var(--text-muted)]">MACD Signal</span>
                <span className="mono">{indicators.macd_signal?.toFixed(4) || '—'}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-[var(--text-muted)]">ADX</span>
                <span className="mono">{indicators.adx?.toFixed(1) || '—'}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-[var(--text-muted)]">ATR (14)</span>
                <span className="mono">{indicators.atr_14?.toFixed(4) || '—'}</span>
              </div>
            </div>
          </div>
          <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Bollinger Bands</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-[var(--text-muted)]">Upper Band</span><span className="mono">{indicators.bb_upper?.toFixed(4) || '—'}</span></div>
              <div className="flex justify-between"><span className="text-[var(--text-muted)]">Middle Band</span><span className="mono">{indicators.bb_middle?.toFixed(4) || '—'}</span></div>
              <div className="flex justify-between"><span className="text-[var(--text-muted)]">Lower Band</span><span className="mono">{indicators.bb_lower?.toFixed(4) || '—'}</span></div>
            </div>
          </div>
          <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Support & Resistance</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-[var(--text-muted)]">Resistance 1</span><span className="mono text-[var(--bearish)]">{indicators.resistance_1?.toFixed(4) || '—'}</span></div>
              <div className="flex justify-between"><span className="text-[var(--text-muted)]">Pivot</span><span className="mono">{indicators.pivot?.toFixed(4) || '—'}</span></div>
              <div className="flex justify-between"><span className="text-[var(--text-muted)]">Support 1</span><span className="mono text-[var(--bullish)]">{indicators.support_1?.toFixed(4) || '—'}</span></div>
            </div>
          </div>
        </div>
        )}
        </div>
      )}


      {/* News Tab */}
      {activeTab === 'news' && (
        <div className="card">
          <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Related News</h3>
          {(!assetNews || assetNews.length === 0) ? (
            <p className="text-sm text-[var(--text-muted)] text-center py-6">No news found for {symbol}</p>
          ) : (
            <div className="space-y-4">
              {assetNews.map((article: any, i: number) => (
                <div key={i} className="py-3 border-b border-[var(--border-primary)] last:border-0">
                  <div className="text-sm font-medium text-[var(--text-primary)]">{article.title}</div>
                  {article.summary && <p className="text-xs text-[var(--text-secondary)] mt-1 leading-relaxed">{article.summary}</p>}
                  <div className="flex flex-wrap gap-2 mt-2">
                    <span className="text-xs text-[var(--text-muted)]">{article.source_name}</span>
                    {article.impact_pathway && (
                      <details className="text-xs">
                        <summary className="text-[var(--text-accent)] cursor-pointer">Impact Pathway</summary>
                        <p className="mt-1 text-[var(--text-secondary)] pl-3 border-l-2 border-[var(--border-accent)]">{article.impact_pathway}</p>
                      </details>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Signal Tab */}
      {activeTab === 'signal' && signal && (
        <div className="space-y-6">
          {/* Component Scores */}
          <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Signal Component Breakdown</h3>
            <div className="space-y-3">
              {[
                ['Technical Score', signal.technical_score],
                ['Fundamental Score', signal.fundamental_score],
                ['News Score', signal.news_score],
                ['Market Context', signal.market_context_score],
                ...(signal.onchain_score != null ? [['On-Chain Score', signal.onchain_score]] : []),
              ].map(([label, value]: any) => (
                <div key={label}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-[var(--text-muted)]">{label}</span>
                    <span className={`mono font-medium ${value > 0 ? 'text-[var(--bullish)]' : value < 0 ? 'text-[var(--bearish)]' : ''}`}>
                      {value?.toFixed(1) || '0'}
                    </span>
                  </div>
                  <ScoreBar value={value || 0} color={value > 0 ? 'var(--bullish)' : value < 0 ? 'var(--bearish)' : 'var(--text-muted)'} />
                </div>
              ))}
              <div className="flex justify-between text-sm pt-2 border-t border-[var(--border-primary)]">
                <span className="text-[var(--text-muted)]">Risk Penalty</span>
                <span className="mono text-[var(--bearish)]">-{signal.risk_penalty?.toFixed(1)}</span>
              </div>
            </div>
          </div>

          {/* Weights Used */}
          <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Weights Used</h3>
            <p className="text-xs text-[var(--text-muted)] mb-2">These weights are configurable and are not claimed to be optimal.</p>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {signal.weights_used && Object.entries(signal.weights_used).map(([key, val]: any) => (
                <div key={key} className="text-xs px-2 py-1.5 rounded bg-[var(--bg-tertiary)]">
                  <span className="text-[var(--text-muted)]">{key}: </span>
                  <span className="mono font-medium">{(val * 100).toFixed(0)}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Risks */}
          <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Key Risks</h3>
            <div className="space-y-2">
              {signal.key_risks?.map((r: any, i: number) => (
                <div key={i} className="flex items-start gap-2 text-sm">
                  <span className="text-[var(--warning)] mt-0.5">⚠</span>
                  <div>
                    <span className="text-[var(--text-primary)]">{r.risk}</span>
                    <span className="text-xs text-[var(--text-muted)] ml-2">({r.severity})</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Data Sources & Metadata */}
          <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Signal Metadata</h3>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div><span className="text-[var(--text-muted)]">Model Version:</span> <span className="mono">{signal.model_version || 'rule_based_v1'}</span></div>
              <div><span className="text-[var(--text-muted)]">Config Version:</span> <span className="mono">{signal.config_version}</span></div>
              <div><span className="text-[var(--text-muted)]">Calculated At:</span> <span className="mono">{new Date(signal.calculation_timestamp).toLocaleString()}</span></div>
              <div><span className="text-[var(--text-muted)]">Expires At:</span> <span className="mono">{signal.expires_at ? new Date(signal.expires_at).toLocaleString() : 'N/A'}</span></div>
              <div><span className="text-[var(--text-muted)]">Data Sources:</span> <span className="mono">{signal.data_sources?.join(', ')}</span></div>
              <div><span className="text-[var(--text-muted)]">Data Quality:</span> <span className="mono">{signal.data_quality_score?.toFixed(0)}/100</span></div>
            </div>
          </div>

          <div className="disclaimer-box">
            <strong>⚠️</strong> {signal.disclaimer}
          </div>
        </div>
      )}
    </div>
  );
}
