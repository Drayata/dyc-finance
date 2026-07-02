'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function AlertsPage() {
  const [loading, setLoading] = useState(true);

  // In a real implementation, you would fetch from /api/alerts
  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 500);
    return () => clearTimeout(timer);
  }, []);

  const mockAlerts = [
    {
      id: '1',
      symbol: 'BTC',
      condition: 'Price drops below',
      value: '$60,000',
      active: true,
      triggered: false
    },
    {
      id: '2',
      symbol: 'AAPL',
      condition: 'Signal changes to',
      value: 'Strong Bullish',
      active: true,
      triggered: false
    },
    {
      id: '3',
      symbol: 'NVDA',
      condition: 'News Sentiment drops below',
      value: 'Neutral',
      active: false,
      triggered: true
    }
  ];

  return (
    <div className="min-h-screen p-4 md:p-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">🔔 Alerts</h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">Get notified about market events</p>
        </div>
        <button className="px-4 py-2 bg-[var(--text-accent)] text-white rounded-lg font-medium hover:opacity-90 transition-opacity">
          + Create Alert
        </button>
      </div>

      {loading ? (
        <div className="space-y-4">
          <div className="skeleton h-20 w-full rounded-xl" />
          <div className="skeleton h-20 w-full rounded-xl" />
          <div className="skeleton h-20 w-full rounded-xl" />
        </div>
      ) : (
        <div className="space-y-4">
          {mockAlerts.map(alert => (
            <div key={alert.id} className={`card flex items-center justify-between p-4 ${alert.triggered ? 'opacity-60' : ''}`}>
              <div className="flex items-center gap-4">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${alert.active ? 'bg-blue-500/20 text-blue-500' : 'bg-[var(--bg-tertiary)] text-[var(--text-muted)]'}`}>
                  🔔
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <Link href={`/asset/${alert.symbol}`} className="font-bold text-[var(--text-primary)] no-underline hover:underline">
                      {alert.symbol}
                    </Link>
                    {alert.triggered && <span className="text-[0.625rem] px-2 py-0.5 rounded-full bg-[var(--warning-bg)] text-[var(--warning)] uppercase tracking-wider font-bold">Triggered</span>}
                  </div>
                  <div className="text-sm text-[var(--text-secondary)]">
                    {alert.condition} <span className="font-semibold text-[var(--text-primary)]">{alert.value}</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <label className="flex items-center cursor-pointer">
                  <div className="relative">
                    <input type="checkbox" className="sr-only" checked={alert.active} readOnly />
                    <div className={`block w-10 h-6 rounded-full transition-colors ${alert.active ? 'bg-[var(--text-accent)]' : 'bg-[var(--bg-tertiary)] border border-[var(--border-primary)]'}`}></div>
                    <div className={`dot absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform ${alert.active ? 'transform translate-x-4' : ''}`}></div>
                  </div>
                </label>
                <button className="text-[var(--text-muted)] hover:text-[var(--bearish)] bg-transparent border-none cursor-pointer text-lg">
                  🗑
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
