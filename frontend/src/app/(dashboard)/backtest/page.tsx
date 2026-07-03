'use client';

import { useState, useEffect } from 'react';
import { markets } from '@/lib/api';

export default function BacktestDashboard() {
  const [backtests, setBacktests] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real implementation, this would fetch from a /api/backtests endpoint.
    // For now, we mock the data to show the UI structure.
    setTimeout(() => {
      setBacktests([
        {
          id: 1,
          asset: 'BTC',
          strategy: 'NLP + MACD Crossover',
          run_date: '2026-07-01T10:00:00Z',
          metrics: {
            total_return: 14.5,
            benchmark_return: 10.2,
            max_drawdown: 5.1,
            win_rate: 62.5,
            sharpe_ratio: 1.8,
            trades_count: 24,
          }
        },
        {
          id: 2,
          asset: 'ETH',
          strategy: 'RSI Mean Reversion',
          run_date: '2026-07-02T08:30:00Z',
          metrics: {
            total_return: -2.4,
            benchmark_return: 1.1,
            max_drawdown: 12.4,
            win_rate: 45.0,
            sharpe_ratio: -0.4,
            trades_count: 18,
          }
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  return (
    <div className="min-h-screen p-4 md:p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">Backtesting Engine</h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">Evaluate strategy performance against historical data.</p>
        </div>
        <button className="px-4 py-2 bg-[var(--text-accent)] text-white text-sm font-medium rounded-lg border-none cursor-pointer hover:opacity-90">
          + New Backtest
        </button>
      </div>

      <div className="card mb-6 bg-[var(--bg-secondary)] border border-[var(--border-primary)]">
        <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-2">About Backtesting</h3>
        <p className="text-sm text-[var(--text-secondary)]">
          The walk-forward backtesting engine simulates trading based on historical signals. It includes a 0.1% slippage assumption per trade. Past performance does not guarantee future results.
        </p>
      </div>

      <div className="space-y-4">
        {loading ? (
          <div className="skeleton h-32 w-full" />
        ) : (
          backtests.map((bt) => (
            <div key={bt.id} className="card flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-bold text-[var(--text-primary)]">{bt.asset}</span>
                  <span className="text-xs px-2 py-1 bg-[var(--bg-tertiary)] rounded-full text-[var(--text-muted)]">{bt.strategy}</span>
                </div>
                <div className="text-xs text-[var(--text-muted)]">Run on: {new Date(bt.run_date).toLocaleString()}</div>
              </div>
              
              <div className="grid grid-cols-3 gap-6 text-right">
                <div>
                  <div className="text-xs text-[var(--text-muted)]">Return</div>
                  <div className={`font-mono font-medium ${bt.metrics.total_return >= 0 ? 'text-[var(--bullish)]' : 'text-[var(--bearish)]'}`}>
                    {bt.metrics.total_return >= 0 ? '+' : ''}{bt.metrics.total_return.toFixed(1)}%
                  </div>
                </div>
                <div>
                  <div className="text-xs text-[var(--text-muted)]">Win Rate</div>
                  <div className="font-mono font-medium text-[var(--text-primary)]">{bt.metrics.win_rate.toFixed(1)}%</div>
                </div>
                <div>
                  <div className="text-xs text-[var(--text-muted)]">Max Drawdown</div>
                  <div className="font-mono font-medium text-[var(--bearish)]">-{bt.metrics.max_drawdown.toFixed(1)}%</div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
