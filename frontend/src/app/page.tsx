'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function RootPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const token = localStorage.getItem('marketpulse_token');
    
    // Using a slight timeout ensures smooth transition without flash
    setTimeout(() => {
      if (token) {
        router.replace('/dashboard');
      } else {
        router.replace('/landing');
      }
    }, 50);
  }, [router]);

  if (!mounted) return null;

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--bg-primary)]">
      {/* Loading state while redirecting */}
      <div className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl animate-pulse" style={{ background: 'var(--gradient-primary)' }}>
        🧠
      </div>
    </div>
  );
}
