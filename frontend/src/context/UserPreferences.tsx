'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

type ViewMode = 'simple' | 'advanced';
type ThemeMode = 'light' | 'dark' | 'system';

interface UserPreferencesContextType {
  viewMode: ViewMode;
  setViewMode: (mode: ViewMode) => void;
  theme: ThemeMode;
  setTheme: (theme: ThemeMode) => void;
}

const UserPreferencesContext = createContext<UserPreferencesContextType | undefined>(undefined);

export function UserPreferencesProvider({ children }: { children: ReactNode }) {
  const [viewMode, setViewModeState] = useState<ViewMode>('advanced');
  const [theme, setThemeState] = useState<ThemeMode>('dark');
  const [mounted, setMounted] = useState(false);

  // Load from local storage on mount
  useEffect(() => {
    const savedMode = localStorage.getItem('marketpulse_viewMode') as ViewMode;
    if (savedMode && (savedMode === 'simple' || savedMode === 'advanced')) {
      setViewModeState(savedMode);
    }
    
    const savedTheme = localStorage.getItem('marketpulse_theme') as ThemeMode;
    if (savedTheme) {
      setThemeState(savedTheme);
    }
    setMounted(true);
  }, []);

  // Update theme classes on document when theme changes
  useEffect(() => {
    if (!mounted) return;
    
    const root = document.documentElement;
    if (theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.add('light');
      root.classList.remove('dark');
    }
    
    localStorage.setItem('marketpulse_theme', theme);
  }, [theme, mounted]);

  const setViewMode = (mode: ViewMode) => {
    setViewModeState(mode);
    localStorage.setItem('marketpulse_viewMode', mode);
  };

  const setTheme = (newTheme: ThemeMode) => {
    setThemeState(newTheme);
  };

  return (
    <UserPreferencesContext.Provider value={{ viewMode, setViewMode, theme, setTheme }}>
      {children}
    </UserPreferencesContext.Provider>
  );
}

export function useUserPreferences() {
  const context = useContext(UserPreferencesContext);
  if (context === undefined) {
    throw new Error('useUserPreferences must be used within a UserPreferencesProvider');
  }
  return context;
}
