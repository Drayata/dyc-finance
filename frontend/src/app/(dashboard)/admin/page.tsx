'use client';

import { useState } from 'react';

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState<'users' | 'system'>('system');

  return (
    <div className="min-h-screen p-4 md:p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-[var(--text-primary)]">Admin Dashboard</h1>
        <p className="text-sm text-[var(--text-secondary)] mt-1">Manage system configurations and users.</p>
      </div>

      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setActiveTab('system')}
          className={`px-4 py-2 rounded-lg text-sm font-medium border-none cursor-pointer ${
            activeTab === 'system' ? 'bg-[var(--text-accent)] text-white' : 'bg-[var(--bg-secondary)] text-[var(--text-secondary)]'
          }`}
        >
          System Config
        </button>
        <button
          onClick={() => setActiveTab('users')}
          className={`px-4 py-2 rounded-lg text-sm font-medium border-none cursor-pointer ${
            activeTab === 'users' ? 'bg-[var(--text-accent)] text-white' : 'bg-[var(--bg-secondary)] text-[var(--text-secondary)]'
          }`}
        >
          Users
        </button>
      </div>

      {activeTab === 'system' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Model Weights Configuration</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-xs text-[var(--text-muted)] mb-1">Technical Score Weight</label>
                <input type="range" min="0" max="100" defaultValue="40" className="w-full accent-[var(--text-accent)]" />
              </div>
              <div>
                <label className="block text-xs text-[var(--text-muted)] mb-1">Fundamental Score Weight</label>
                <input type="range" min="0" max="100" defaultValue="30" className="w-full accent-[var(--text-accent)]" />
              </div>
              <div>
                <label className="block text-xs text-[var(--text-muted)] mb-1">News Sentiment Weight</label>
                <input type="range" min="0" max="100" defaultValue="20" className="w-full accent-[var(--text-accent)]" />
              </div>
              <div>
                <label className="block text-xs text-[var(--text-muted)] mb-1">Market Context Weight</label>
                <input type="range" min="0" max="100" defaultValue="10" className="w-full accent-[var(--text-accent)]" />
              </div>
              <button className="w-full mt-4 py-2 bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] rounded-lg text-sm font-medium hover:bg-[var(--bg-tertiary)] cursor-pointer">
                Save Weights
              </button>
            </div>
          </div>

          <div className="card">
            <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-4">System Status</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center text-sm">
                <span className="text-[var(--text-secondary)]">Database</span>
                <span className="text-[var(--bullish)] px-2 py-1 bg-[var(--bullish-bg)] rounded text-xs font-bold">Connected</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-[var(--text-secondary)]">Redis Cache</span>
                <span className="text-[var(--bullish)] px-2 py-1 bg-[var(--bullish-bg)] rounded text-xs font-bold">Connected</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-[var(--text-secondary)]">News Pipeline</span>
                <span className="text-[var(--bullish)] px-2 py-1 bg-[var(--bullish-bg)] rounded text-xs font-bold">Active</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-[var(--text-secondary)]">API Rate Limits</span>
                <span className="text-[var(--text-muted)] mono text-xs">45/100/min</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'users' && (
        <div className="card">
          <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-4">User Management</h3>
          <div className="text-center py-8 text-[var(--text-muted)] text-sm">
            Admin user list will be displayed here.
          </div>
        </div>
      )}
    </div>
  );
}
