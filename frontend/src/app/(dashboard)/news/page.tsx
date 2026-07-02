'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { news as newsApi } from '@/lib/api';

export default function NewsIntelligencePage() {
  const [articles, setArticles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>('');
  const [directionFilter, setDirectionFilter] = useState<string>('');
  const [verifiedOnly, setVerifiedOnly] = useState<boolean>(false);

  useEffect(() => {
    async function fetchNews() {
      try {
        setLoading(true);
        const params: Record<string, string> = { limit: '30' };
        if (categoryFilter) params.event_category = categoryFilter;
        if (directionFilter) params.impact_direction = directionFilter;
        if (verifiedOnly) params.is_verified = 'true';

        const result: any = await newsApi.list(params);
        setArticles(result?.items || []);
        setError(null);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchNews();
  }, [categoryFilter, directionFilter, verifiedOnly]);

  const sentimentColor = (s: number) => s > 0.3 ? 'var(--bullish)' : s < -0.3 ? 'var(--bearish)' : 'var(--text-muted)';

  return (
    <div className="min-h-screen p-4 md:p-6">
      <Link href="/" className="text-[var(--text-accent)] text-sm mb-4 block no-underline hover:underline">← Dashboard</Link>

      <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-1">📰 News Intelligence</h1>
      <p className="text-sm text-[var(--text-secondary)] mb-6">Market-moving news with impact analysis and entity extraction</p>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="px-3 py-2 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] text-sm focus:outline-none"
        >
          <option value="">All Categories</option>
          <option value="earnings">Earnings</option>
          <option value="interest_rate">Interest Rate</option>
          <option value="regulatory_action">Regulatory</option>
          <option value="etf_flow">ETF Flow</option>
          <option value="protocol_upgrade">Protocol Upgrade</option>
          <option value="token_unlock">Token Unlock</option>
          <option value="strategic_partnership">Partnership</option>
          <option value="rumor">Rumor</option>
        </select>
        <select
          value={directionFilter}
          onChange={(e) => setDirectionFilter(e.target.value)}
          className="px-3 py-2 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] text-sm focus:outline-none"
        >
          <option value="">All Directions</option>
          <option value="bullish">Bullish</option>
          <option value="bearish">Bearish</option>
          <option value="neutral">Neutral</option>
          <option value="mixed">Mixed</option>
          <option value="uncertain">Uncertain</option>
        </select>
        <label className="flex items-center gap-2 text-sm text-[var(--text-secondary)] cursor-pointer">
          <input
            type="checkbox"
            checked={verifiedOnly}
            onChange={(e) => setVerifiedOnly(e.target.checked)}
            className="rounded"
          />
          Verified only
        </label>
      </div>

      {error && (
        <div className="card mb-4" style={{ background: 'var(--bearish-bg)' }}>
          <p className="text-[var(--bearish)] text-sm">Error: {error}</p>
        </div>
      )}

      {loading ? (
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => <div key={i} className="skeleton h-32 rounded-xl" />)}
        </div>
      ) : (
        <div className="space-y-4">
          {articles.length === 0 ? (
            <div className="card text-center py-8">
              <p className="text-[var(--text-muted)]">No news articles match the current filters.</p>
            </div>
          ) : (
            articles.map((article: any, i: number) => (
              <div key={i} className="card hover:border-[var(--border-accent)] transition-all">
                {/* Header */}
                <div className="flex items-start gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      {!article.is_verified && (
                        <span className="text-xs px-2 py-0.5 rounded-full font-medium" style={{ background: 'var(--warning-bg)', color: 'var(--warning)' }}>
                          ⚠ UNVERIFIED
                        </span>
                      )}
                      {article.event_category && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--bg-tertiary)] text-[var(--text-muted)]">
                          {article.event_category.replace(/_/g, ' ')}
                        </span>
                      )}
                    </div>
                    <h3 className="text-base font-semibold text-[var(--text-primary)] leading-tight">{article.title}</h3>
                  </div>
                </div>

                {/* Summary */}
                {article.summary && (
                  <p className="text-sm text-[var(--text-secondary)] mt-2 leading-relaxed">{article.summary}</p>
                )}

                {/* Metrics Row */}
                <div className="flex flex-wrap gap-3 mt-3 text-xs">
                  <span className="text-[var(--text-muted)]">📰 {article.source_name}</span>
                  <span className="text-[var(--text-muted)]">
                    🕐 {new Date(article.published_at).toLocaleString()}
                  </span>
                  {article.impact_score != null && (
                    <span className="text-[var(--text-muted)]">
                      Impact: <span className="mono font-medium text-[var(--text-primary)]">{article.impact_score}/100</span>
                    </span>
                  )}
                  {article.overall_sentiment != null && (
                    <span style={{ color: sentimentColor(article.overall_sentiment) }}>
                      Sentiment: <span className="mono font-medium">{article.overall_sentiment > 0 ? '+' : ''}{article.overall_sentiment.toFixed(2)}</span>
                    </span>
                  )}
                  {article.impact_direction && (
                    <span className={`capitalize font-medium ${
                      article.impact_direction === 'bullish' ? 'text-[var(--bullish)]' :
                      article.impact_direction === 'bearish' ? 'text-[var(--bearish)]' :
                      'text-[var(--text-muted)]'
                    }`}>
                      {article.impact_direction}
                    </span>
                  )}
                  {article.impact_time_horizon && (
                    <span className="text-[var(--text-muted)]">⏱ {article.impact_time_horizon.replace(/_/g, ' ')}</span>
                  )}
                  {article.source_credibility_score != null && (
                    <span className="text-[var(--text-muted)]">Credibility: {article.source_credibility_score}/100</span>
                  )}
                </div>

                {/* Related Assets */}
                {article.related_assets && article.related_assets.length > 0 && (
                  <div className="flex gap-1.5 mt-3 flex-wrap">
                    {article.related_assets.map((symbol: string) => (
                      <Link
                        key={symbol}
                        href={`/asset/${symbol}`}
                        className="text-xs px-2 py-1 rounded-md bg-[var(--bg-tertiary)] text-[var(--text-accent)] no-underline hover:bg-[var(--border-secondary)] transition-colors font-medium"
                      >
                        {symbol}
                      </Link>
                    ))}
                  </div>
                )}

                {/* Impact Pathway */}
                {article.impact_pathway && (
                  <details className="mt-3">
                    <summary className="text-xs text-[var(--text-accent)] cursor-pointer font-medium">
                      📊 View Impact Pathway
                    </summary>
                    <div className="mt-2 text-xs text-[var(--text-secondary)] pl-3 py-2 border-l-2 border-[var(--border-accent)] bg-[var(--bg-tertiary)] rounded-r-lg">
                      {article.impact_pathway}
                    </div>
                  </details>
                )}
              </div>
            ))
          )}
        </div>
      )}

      <div className="disclaimer-box mt-6">
        <strong>⚠️</strong> News analysis is automated and may contain errors. Sentiment and impact scores are probabilistic estimates, not certainties. Always verify information from primary sources. Unverified content is clearly labeled.
      </div>
    </div>
  );
}
