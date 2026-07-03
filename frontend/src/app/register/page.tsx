'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { auth } from '@/lib/api';

export default function RegisterPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [agreedToTerms, setAgreedToTerms] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (!agreedToTerms) {
      setError('You must agree to the Terms of Service and Disclaimer');
      return;
    }

    setLoading(true);

    try {
      await auth.register({ username, email, password });
      
      const loginRes: any = await auth.login({ email, password });
      
      localStorage.setItem('marketpulse_token', loginRes.access_token);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--bg-primary)] p-4 py-12">
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
          <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-2">Create an account</h1>
          <p className="text-sm text-[var(--text-secondary)] mb-6">Get access to AI-driven market intelligence</p>

          {error && (
            <div className="mb-4 p-3 rounded-lg text-sm bg-[var(--bearish-bg)] text-[var(--bearish)] border border-[var(--bearish-border)]">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">Username</label>
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2.5 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] focus:outline-none focus:border-[var(--text-accent)] transition-colors"
                placeholder="trader123"
              />
            </div>

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
              <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">Password</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2.5 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] focus:outline-none focus:border-[var(--text-accent)] transition-colors"
                placeholder="••••••••"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">Confirm Password</label>
              <input
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-2.5 rounded-lg bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] focus:outline-none focus:border-[var(--text-accent)] transition-colors"
                placeholder="••••••••"
              />
            </div>

            <div className="pt-2">
              <label className="flex items-start gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={agreedToTerms}
                  onChange={(e) => setAgreedToTerms(e.target.checked)}
                  className="mt-1"
                />
                <span className="text-xs text-[var(--text-secondary)] leading-tight">
                  I agree to the <Link href="/terms" className="text-[var(--text-accent)] hover:underline">Terms of Service</Link> and understand the <Link href="/disclaimer" className="text-[var(--text-accent)] hover:underline">Financial Disclaimer</Link>. I acknowledge that MarketPulse AI is not a licensed financial advisor.
                </span>
              </label>
            </div>

            <button
              type="submit"
              disabled={loading || !agreedToTerms}
              className="w-full py-2.5 px-4 bg-[var(--text-accent)] text-white rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed mt-4"
            >
              {loading ? 'Creating account...' : 'Create account'}
            </button>
          </form>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-[var(--text-secondary)] mt-6">
          Already have an account?{' '}
          <Link href="/login" className="text-[var(--text-accent)] no-underline hover:underline font-medium">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
