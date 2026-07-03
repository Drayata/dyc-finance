'use client';

import { useState } from 'react';
import { useUserPreferences } from '@/context/UserPreferences';

export default function SettingsPage() {
  const { theme, setTheme, viewMode, setViewMode } = useUserPreferences();
  const [emailNotifs, setEmailNotifs] = useState(true);

  return (
    <div className="min-h-screen p-4 md:p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-6">⚙️ Settings</h1>
      
      <div className="space-y-6">
        {/* Appearance */}
        <div className="card">
          <h2 className="text-lg font-bold text-[var(--text-primary)] mb-4 border-b border-[var(--border-primary)] pb-2">Appearance</h2>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-[var(--text-primary)]">Theme</div>
                <div className="text-sm text-[var(--text-secondary)]">Choose how the application looks.</div>
              </div>
              <select 
                value={theme} 
                onChange={(e) => setTheme(e.target.value as 'light' | 'dark' | 'system')}
                className="px-3 py-2 bg-[var(--bg-secondary)] border border-[var(--border-primary)] rounded-lg text-[var(--text-primary)] focus:outline-none focus:border-[var(--text-accent)]"
              >
                <option value="dark">Dark</option>
                <option value="light">Light</option>
                <option value="system">System</option>
              </select>
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-[var(--text-primary)]">View Mode</div>
                <div className="text-sm text-[var(--text-secondary)]">Simple hides advanced indicators and metadata.</div>
              </div>
              <div className="flex bg-[var(--bg-secondary)] border border-[var(--border-primary)] rounded-lg overflow-hidden">
                <button 
                  onClick={() => setViewMode('simple')}
                  className={`px-4 py-2 text-sm border-none cursor-pointer ${viewMode === 'simple' ? 'bg-[var(--text-accent)] text-white' : 'bg-transparent text-[var(--text-secondary)] hover:bg-[var(--bg-tertiary)]'}`}
                >
                  Simple
                </button>
                <button 
                  onClick={() => setViewMode('advanced')}
                  className={`px-4 py-2 text-sm border-none cursor-pointer ${viewMode === 'advanced' ? 'bg-[var(--text-accent)] text-white' : 'bg-transparent text-[var(--text-secondary)] hover:bg-[var(--bg-tertiary)]'}`}
                >
                  Advanced
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Notifications */}
        <div className="card">
          <h2 className="text-lg font-bold text-[var(--text-primary)] mb-4 border-b border-[var(--border-primary)] pb-2">Notifications</h2>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-[var(--text-primary)]">Email Notifications</div>
                <div className="text-sm text-[var(--text-secondary)]">Receive triggered alerts via email.</div>
              </div>
              <label className="flex items-center cursor-pointer">
                <div className="relative">
                  <input type="checkbox" className="sr-only" checked={emailNotifs} onChange={() => setEmailNotifs(!emailNotifs)} />
                  <div className={`block w-10 h-6 rounded-full transition-colors ${emailNotifs ? 'bg-[var(--text-accent)]' : 'bg-[var(--bg-tertiary)] border border-[var(--border-primary)]'}`}></div>
                  <div className={`dot absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform ${emailNotifs ? 'transform translate-x-4' : ''}`}></div>
                </div>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
