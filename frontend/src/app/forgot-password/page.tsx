'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    // In a real app, you would call auth.forgotPassword(email)
    // We simulate a network delay here
    setTimeout(() => {
      setLoading(false);
      setSubmitted(true);
    }, 1000);
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
          <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-2">Reset Password</h1>
          
          {submitted ? (
            <div className="text-center py-4">
              <div className="w-12 h-12 rounded-full bg-[var(--bullish-bg)] text-[var(--bullish)] flex items-center justify-center text-2xl mx-auto mb-4">
                ✓
              </div>
              <p className="text-sm text-[var(--text-secondary)] mb-6">
                If an account exists for <strong>{email}</strong>, we have sent a password reset link to it.
              </p>
              <Link href="/login" className="block w-full py-2.5 px-4 bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-lg font-medium hover:bg-[var(--border-secondary)] transition-colors no-underline">
                Return to Login
              </Link>
            </div>
          ) : (
            <>
              <p className="text-sm text-[var(--text-secondary)] mb-6">
                Enter the email address associated with your account and we'll send you a link to reset your password.
              </p>

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

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-2.5 px-4 bg-[var(--text-accent)] text-white rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed mt-2"
                >
                  {loading ? 'Sending link...' : 'Send reset link'}
                </button>
              </form>
            </>
          )}
        </div>

        {/* Footer */}
        {!submitted && (
          <p className="text-center text-sm text-[var(--text-secondary)] mt-6">
            Remember your password?{' '}
            <Link href="/login" className="text-[var(--text-accent)] no-underline hover:underline font-medium">
              Sign in
            </Link>
          </p>
        )}
      </div>
    </div>
  );
}
