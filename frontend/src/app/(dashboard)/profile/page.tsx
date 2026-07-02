'use client';

export default function ProfilePage() {
  return (
    <div className="min-h-screen p-4 md:p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-6">👤 Profile</h1>
      
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-1 space-y-6">
          {/* User Info Card */}
          <div className="card text-center">
            <div className="w-24 h-24 rounded-full bg-[var(--bg-tertiary)] flex items-center justify-center text-[var(--text-primary)] font-bold text-4xl mx-auto mb-4 border-4 border-[var(--bg-secondary)] shadow-lg">
              U
            </div>
            <h2 className="text-xl font-bold text-[var(--text-primary)]">Demo User</h2>
            <p className="text-sm text-[var(--text-secondary)] mb-4">demo@example.com</p>
            
            <div className="inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-[var(--text-accent)] text-white shadow-md shadow-blue-500/20 mb-4">
              Pro Plan
            </div>
            
            <div className="border-t border-[var(--border-primary)] pt-4 mt-2">
              <button className="text-sm text-[var(--bearish)] hover:underline bg-transparent border-none cursor-pointer">
                Sign Out
              </button>
            </div>
          </div>
        </div>

        <div className="md:col-span-2 space-y-6">
          {/* Subscription Info */}
          <div className="card">
            <div className="flex justify-between items-center mb-4 border-b border-[var(--border-primary)] pb-2">
              <h2 className="text-lg font-bold text-[var(--text-primary)]">Subscription</h2>
              <button className="text-xs bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] px-3 py-1.5 rounded hover:bg-[var(--bg-tertiary)] cursor-pointer">
                Manage Billing
              </button>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-[var(--text-secondary)]">Current Plan</span>
                <span className="font-medium text-[var(--text-primary)]">MarketPulse Pro</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-[var(--text-secondary)]">Billing Cycle</span>
                <span className="font-medium text-[var(--text-primary)]">Monthly ($49.00/mo)</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-[var(--text-secondary)]">Next Payment</span>
                <span className="font-medium text-[var(--text-primary)]">Aug 02, 2026</span>
              </div>
              
              <div className="mt-4 pt-4 border-t border-[var(--border-primary)]">
                <div className="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider mb-2">Usage Limits (Monthly)</div>
                
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-[var(--text-secondary)]">Custom Alerts</span>
                      <span className="font-medium text-[var(--text-primary)]">12 / 50</span>
                    </div>
                    <div className="w-full bg-[var(--bg-secondary)] rounded-full h-1.5">
                      <div className="bg-[var(--text-accent)] h-1.5 rounded-full" style={{ width: '24%' }}></div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-[var(--text-secondary)]">Watchlists</span>
                      <span className="font-medium text-[var(--text-primary)]">2 / 10</span>
                    </div>
                    <div className="w-full bg-[var(--bg-secondary)] rounded-full h-1.5">
                      <div className="bg-[var(--text-accent)] h-1.5 rounded-full" style={{ width: '20%' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Security */}
          <div className="card">
            <h2 className="text-lg font-bold text-[var(--text-primary)] mb-4 border-b border-[var(--border-primary)] pb-2">Security</h2>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium text-[var(--text-primary)]">Password</div>
                  <div className="text-sm text-[var(--text-secondary)]">Last changed 3 months ago</div>
                </div>
                <button className="px-4 py-2 text-sm bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] rounded-lg hover:bg-[var(--bg-tertiary)] cursor-pointer">
                  Update
                </button>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium text-[var(--text-primary)]">Two-Factor Authentication</div>
                  <div className="text-sm text-[var(--text-secondary)]">Add an extra layer of security</div>
                </div>
                <button className="px-4 py-2 text-sm bg-[var(--bg-secondary)] border border-[var(--border-primary)] text-[var(--text-primary)] rounded-lg hover:bg-[var(--bg-tertiary)] cursor-pointer">
                  Enable
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
