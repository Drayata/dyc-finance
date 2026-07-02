'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { markets } from '@/lib/api';

export default function AssetScreenerPage() {
  const [assets, setAssets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [assetType, setAssetType] = useState<string>('');
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    async function fetchAssets() {
      try {
        setLoading(true);
        const params: Record<string, string> = {
          page: String(page),
          page_size: '20',
          sort_by: sortBy,
          sort_order: sortOrder,
        };
        if (assetType) params.asset_type = assetType;
        if (search) params.search = search;

        const result: any = await markets.listAssets(params);
        setAssets(result?.items || []);
        setTotalPages(result?.total_pages || 1);
        setError(null);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchAssets();
  }, [assetType, search, sortBy, sortOrder, page]);

  return (
    <div className="min-h-screen p-4 md:p-6">
      <Link href="/" className="text-[var(--text-accent)] text-sm mb-4 block no-underline hover:underline">← Dashboard</Link>

      <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-1">🔍 Asset Screener</h1>
      <p className="text-sm text-[var(--text-secondary)] mb-6">Filter and explore stocks and cryptocurrencies</p>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <input
          type="text"
          placeholder="Search symbol or name..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1); }}
          className="px-3 py-2 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] text-sm focus:outline-none focus:border-[var(--text-accent)] w-64"
        />
        <select
          value={assetType}
          onChange={(e) => { setAssetType(e.target.value); setPage(1); }}
          className="px-3 py-2 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] text-sm focus:outline-none"
        >
          <option value="">All Types</option>
          <option value="stock">Stocks</option>
          <option value="crypto">Crypto</option>
        </select>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="px-3 py-2 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] text-sm focus:outline-none"
        >
          <option value="name">Name</option>
          <option value="symbol">Symbol</option>
          <option value="market_cap">Market Cap</option>
          <option value="change_pct">Change %</option>
        </select>
        <button
          onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
          className="px-3 py-2 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] text-sm cursor-pointer hover:bg-[var(--bg-tertiary)]"
        >
          {sortOrder === 'asc' ? '↑ Asc' : '↓ Desc'}
        </button>
      </div>

      {error && (
        <div className="card mb-4" style={{ background: 'var(--bearish-bg)' }}>
          <p className="text-[var(--bearish)] text-sm">Error: {error}</p>
        </div>
      )}

      {/* Asset Table */}
      <div className="card overflow-hidden">
        <div className="table-responsive">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-xs text-[var(--text-muted)] border-b border-[var(--border-primary)]">
                <th className="text-left py-3 px-4 font-medium">Symbol</th>
                <th className="text-left py-3 px-4 font-medium">Name</th>
                <th className="text-left py-3 px-4 font-medium">Type</th>
                <th className="text-left py-3 px-4 font-medium">Sector</th>
                <th className="text-right py-3 px-4 font-medium">Price</th>
                <th className="text-right py-3 px-4 font-medium">Change</th>
                <th className="text-right py-3 px-4 font-medium">Market Cap</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                [...Array(10)].map((_, i) => (
                  <tr key={i} className="border-b border-[var(--border-primary)]">
                    {[...Array(7)].map((_, j) => (
                      <td key={j} className="py-3 px-4"><div className="skeleton h-4 w-20" /></td>
                    ))}
                  </tr>
                ))
              ) : assets.length === 0 ? (
                <tr><td colSpan={7} className="text-center py-8 text-[var(--text-muted)]">No assets found</td></tr>
              ) : (
                assets.map((asset: any, i: number) => (
                  <tr key={i} className="border-b border-[var(--border-primary)] last:border-0 hover:bg-[var(--bg-tertiary)] transition-colors">
                    <td className="py-3 px-4">
                      <Link href={`/asset/${asset.symbol}`} className="text-[var(--text-accent)] no-underline hover:underline font-semibold">
                        {asset.symbol}
                      </Link>
                    </td>
                    <td className="py-3 px-4 text-[var(--text-primary)]">{asset.name}</td>
                    <td className="py-3 px-4">
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        asset.asset_type === 'crypto' ? 'bg-purple-500/20 text-purple-400' : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        {asset.asset_type}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-[var(--text-muted)] text-xs">{asset.sector || '—'}</td>
                    <td className="py-3 px-4 text-right mono">{asset.price ? `$${Number(asset.price).toLocaleString()}` : '—'}</td>
                    <td className="py-3 px-4 text-right">
                      <span className={`mono ${(asset.change_pct || 0) >= 0 ? 'text-[var(--bullish)]' : 'text-[var(--bearish)]'}`}>
                        {(asset.change_pct || 0) >= 0 ? '+' : ''}{(asset.change_pct || 0).toFixed(2)}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right mono text-[var(--text-muted)]">
                      {asset.market_cap ? `$${(asset.market_cap / 1e9).toFixed(1)}B` : '—'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2 mt-4">
          <button
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="px-3 py-1.5 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-sm text-[var(--text-primary)] cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            ← Prev
          </button>
          <span className="text-sm text-[var(--text-muted)]">Page {page} of {totalPages}</span>
          <button
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages}
            className="px-3 py-1.5 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-sm text-[var(--text-primary)] cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
}
