'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { auth } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const response: any = await auth.login({ email, password });
      
      // Store token (in a real app, prefer HttpOnly cookies via Next.js API route)
      localStorage.setItem('marketpulse_token', response.access_token);
      
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--bg-primary)] p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-3 no-underline justify-center">
            <div className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl" style={{ background: 'var(--gradient-primary)' }}>
              🧠
            </div>
            <div className="text-left">
              <div className="text-xl font-bold text-[var(--text-primary)] leading-tight">MarketPulse</div>
              <div className="text-sm text-[var(--text-accent)] font-medium">AI Intelligence</div>
            </div>
          </Link>
        </div>

        {/* Card */}
        <div className="card p-6 md:p-8">
          <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-2">Welcome back</h1>
          <p className="text-sm text-[var(--text-secondary)] mb-6">Enter your credentials to access your dashboard</p>

          {error && (
            <div className="mb-4 p-3 rounded-lg text-sm bg-[var(--bearish-bg)] text-[var(--bearish)] border border-[var(--bearish-border)]">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">Email</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2.5 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] focus:outline-none focus:border-[var(--text-accent)] transition-colors"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="block text-sm font-medium text-[var(--text-primary)]">Password</label>
                <Link href="/forgot-password" className="text-xs text-[var(--text-accent)] no-underline hover:underline">
                  Forgot password?
                </Link>
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2.5 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] focus:outline-none focus:border-[var(--text-accent)] transition-colors"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 px-4 bg-[var(--text-accent)] text-white rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed mt-2"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-[var(--text-secondary)] mt-6">
          Don't have an account?{' '}
          <Link href="/register" className="text-[var(--text-accent)] no-underline hover:underline font-medium">
            Sign up
          </Link>
        </p>

        <div className="text-center text-xs text-[var(--text-muted)] mt-12 max-w-sm mx-auto">
          ⚠️ By signing in, you acknowledge that MarketPulse AI provides educational market analysis, not financial advice.
        </div>
      </div>
    </div>
  );
}
