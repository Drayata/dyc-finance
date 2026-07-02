'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function WatchlistsPage() {
  const [loading, setLoading] = useState(true);

  // In a real implementation, you would fetch from /api/watchlists
  // For the MVP frontend, we show a mock UI of what it will look like
  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 500);
    return () => clearTimeout(timer);
  }, []);

  const mockWatchlists = [
    {
      id: '1',
      name: 'Tech Giants',
      description: 'Major US tech companies',
      items: [
        { symbol: 'AAPL', name: 'Apple Inc.', price: 175.42, change: 1.2 },
        { symbol: 'MSFT', name: 'Microsoft', price: 380.20, change: -0.5 },
        { symbol: 'NVDA', name: 'NVIDIA', price: 850.10, change: 2.4 },
      ]
    },
    {
      id: '2',
      name: 'Crypto Watch',
      description: 'Top crypto assets',
      items: [
        { symbol: 'BTC', name: 'Bitcoin', price: 65430.00, change: 5.2 },
        { symbol: 'ETH', name: 'Ethereum', price: 3450.00, change: 3.1 },
      ]
    }
  ];

  return (
    <div className="min-h-screen p-4 md:p-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">⭐ Watchlists</h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">Track your favorite assets</p>
        </div>
        <button className="px-4 py-2 bg-[var(--text-accent)] text-white rounded-lg font-medium hover:opacity-90 transition-opacity">
          + New Watchlist
        </button>
      </div>

      {loading ? (
        <div className="space-y-4">
          <div className="skeleton h-48 w-full rounded-xl" />
          <div className="skeleton h-48 w-full rounded-xl" />
        </div>
      ) : (
        <div className="space-y-6">
          {mockWatchlists.map(list => (
            <div key={list.id} className="card p-0 overflow-hidden">
              <div className="p-4 border-b border-[var(--border-primary)] flex justify-between items-center bg-[var(--bg-tertiary)]">
                <div>
                  <h3 className="font-bold text-[var(--text-primary)]">{list.name}</h3>
                  <p className="text-xs text-[var(--text-secondary)]">{list.description}</p>
                </div>
                <button className="text-[var(--text-muted)] hover:text-[var(--text-primary)] bg-transparent border-none cursor-pointer">
                  ⋮
                </button>
              </div>
              <div className="table-responsive">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-xs text-[var(--text-muted)] border-b border-[var(--border-primary)] bg-[var(--bg-primary)]">
                      <th className="text-left py-2 px-4 font-medium">Asset</th>
                      <th className="text-right py-2 px-4 font-medium">Price</th>
                      <th className="text-right py-2 px-4 font-medium">Change</th>
                      <th className="text-right py-2 px-4 font-medium">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {list.items.map((item, i) => (
                      <tr key={i} className="border-b border-[var(--border-primary)] last:border-0 hover:bg-[var(--bg-tertiary)] transition-colors">
                        <td className="py-3 px-4">
                          <Link href={`/asset/${item.symbol}`} className="font-bold text-[var(--text-accent)] no-underline hover:underline">
                            {item.symbol}
                          </Link>
                          <span className="ml-2 text-xs text-[var(--text-muted)]">{item.name}</span>
                        </td>
                        <td className="py-3 px-4 text-right mono text-[var(--text-primary)]">
                          ${item.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <span className={`mono ${item.change >= 0 ? 'text-[var(--bullish)]' : 'text-[var(--bearish)]'}`}>
                            {item.change >= 0 ? '+' : ''}{item.change}%
                          </span>
                        </td>
                        <td className="py-3 px-4 text-right">
                          <button className="text-xs text-[var(--bearish)] hover:underline bg-transparent border-none cursor-pointer">Remove</button>
                        </td>
                      </tr>
                    ))}
                    <tr className="bg-[var(--bg-primary)]">
                      <td colSpan={4} className="py-2 px-4 text-center">
                        <button className="text-xs text-[var(--text-accent)] hover:underline bg-transparent border-none cursor-pointer">
                          + Add Asset to Watchlist
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
