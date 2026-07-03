'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import React, { useState } from 'react';
import { UserPreferencesProvider } from '@/context/UserPreferences';

function MobileHeader() {
  const [menuOpen, setMenuOpen] = useState(false);
  return (
    <header className="md:hidden sticky top-0 z-50 bg-[var(--bg-secondary)] border-b border-[var(--border-primary)] px-4 py-3 flex items-center justify-between">
      <Link href="/dashboard" className="flex items-center gap-2 no-underline">
        <span className="text-lg">🧠</span>
        <span className="font-bold text-[var(--text-primary)]">MarketPulse AI</span>
      </Link>
      <button onClick={() => setMenuOpen(!menuOpen)} className="text-2xl bg-transparent border-none cursor-pointer text-[var(--text-primary)]">
        {menuOpen ? '✕' : '☰'}
      </button>
      {menuOpen && (
        <div className="absolute top-full left-0 right-0 bg-[var(--bg-secondary)] border-b border-[var(--border-primary)] p-4 space-y-2 shadow-lg">
          <Link href="/dashboard" className="block px-3 py-2 rounded-lg text-[var(--text-primary)] no-underline hover:bg-[var(--bg-tertiary)]" onClick={() => setMenuOpen(false)}>📊 Dashboard</Link>
          <Link href="/assets" className="block px-3 py-2 rounded-lg text-[var(--text-primary)] no-underline hover:bg-[var(--bg-tertiary)]" onClick={() => setMenuOpen(false)}>🔍 Screener</Link>
          <Link href="/signals" className="block px-3 py-2 rounded-lg text-[var(--text-primary)] no-underline hover:bg-[var(--bg-tertiary)]" onClick={() => setMenuOpen(false)}>📡 Signals</Link>
          <Link href="/news" className="block px-3 py-2 rounded-lg text-[var(--text-primary)] no-underline hover:bg-[var(--bg-tertiary)]" onClick={() => setMenuOpen(false)}>📰 News</Link>
          <div className="my-2 border-b border-[var(--border-primary)]"></div>
          <Link href="/watchlists" className="block px-3 py-2 rounded-lg text-[var(--text-primary)] no-underline hover:bg-[var(--bg-tertiary)]" onClick={() => setMenuOpen(false)}>⭐ Watchlists</Link>
          <Link href="/alerts" className="block px-3 py-2 rounded-lg text-[var(--text-primary)] no-underline hover:bg-[var(--bg-tertiary)]" onClick={() => setMenuOpen(false)}>🔔 Alerts</Link>
          <Link href="/settings" className="block px-3 py-2 rounded-lg text-[var(--text-primary)] no-underline hover:bg-[var(--bg-tertiary)]" onClick={() => setMenuOpen(false)}>⚙️ Settings</Link>
        </div>
      )}
    </header>
  );
}

function Sidebar() {
  const pathname = usePathname();
  const navItems = [
    { href: '/dashboard', label: 'Dashboard', icon: '📊' },
    { href: '/assets', label: 'Screener', icon: '🔍' },
    { href: '/signals', label: 'Signals', icon: '📡' },
    { href: '/news', label: 'News', icon: '📰' },
    { href: '/watchlists', label: 'Watchlists', icon: '⭐' },
    { href: '/alerts', label: 'Alerts', icon: '🔔' },
  ];

  return (
    <aside className="fixed left-0 top-0 h-screen w-[240px] bg-[var(--bg-secondary)] border-r border-[var(--border-primary)] flex-col z-40 hidden md:flex">
      {/* Logo */}
      <div className="p-5 border-b border-[var(--border-primary)]">
        <Link href="/dashboard" className="flex items-center gap-3 no-underline">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center text-lg" style={{ background: 'var(--gradient-primary)' }}>
            🧠
          </div>
          <div>
            <div className="text-base font-bold text-[var(--text-primary)]">MarketPulse</div>
            <div className="text-xs text-[var(--text-accent)] font-medium">AI Intelligence</div>
          </div>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm no-underline transition-all ${
              pathname === item.href || (pathname.startsWith(item.href) && item.href !== '/dashboard')
                ? 'bg-[var(--bg-tertiary)] text-[var(--text-accent)] font-medium'
                : 'text-[var(--text-secondary)] hover:bg-[var(--bg-tertiary)] hover:text-[var(--text-primary)]'
            }`}
          >
            <span className="text-base">{item.icon}</span>
            {item.label}
          </Link>
        ))}

        <div className="pt-4 mt-4 border-t border-[var(--border-primary)]">
          <div className="px-3 mb-2 text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider">Account</div>
          <Link
            href="/settings"
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm no-underline transition-all ${
              pathname === '/settings'
                ? 'bg-[var(--bg-tertiary)] text-[var(--text-accent)] font-medium'
                : 'text-[var(--text-secondary)] hover:bg-[var(--bg-tertiary)] hover:text-[var(--text-primary)]'
            }`}
          >
            <span className="text-base">⚙️</span>
            Settings
          </Link>
          <Link
            href="/profile"
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm no-underline transition-all ${
              pathname === '/profile'
                ? 'bg-[var(--bg-tertiary)] text-[var(--text-accent)] font-medium'
                : 'text-[var(--text-secondary)] hover:bg-[var(--bg-tertiary)] hover:text-[var(--text-primary)]'
            }`}
          >
            <span className="text-base">👤</span>
            Profile
          </Link>
        </div>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-[var(--border-primary)]">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-[var(--bg-tertiary)] flex items-center justify-center text-[var(--text-primary)] font-bold text-sm">
            U
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium text-[var(--text-primary)] truncate">User</div>
            <div className="text-xs text-[var(--text-muted)] truncate">Pro Plan</div>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <UserPreferencesProvider>
      <div className="min-h-screen bg-[var(--bg-primary)]">
        <Sidebar />
        <MobileHeader />
        <div className="md:ml-[240px]">
          {children}
        </div>
      </div>
    </UserPreferencesProvider>
  );
}
