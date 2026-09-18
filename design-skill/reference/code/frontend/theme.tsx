import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import { getTelegramWebApp, paintChrome } from '../telegram/telegram';

export type ThemeChoice = 'system' | 'light' | 'dark';
type Resolved = 'light' | 'dark';

const STORAGE_KEY = 'anonka.theme';
const CHROME: Record<Resolved, string> = { light: '#f8f5f1', dark: '#0f1116' };

interface ThemeState {
  choice: ThemeChoice;
  resolved: Resolved;
  setChoice: (choice: ThemeChoice) => void;
}

const ThemeContext = createContext<ThemeState | null>(null);

function readChoice(): ThemeChoice {
  try {
    const value = localStorage.getItem(STORAGE_KEY);
    return value === 'light' || value === 'dark' ? value : 'system';
  } catch {
    return 'system';
  }
}

function systemScheme(): Resolved {
  const scheme = getTelegramWebApp()?.colorScheme;
  if (scheme && getTelegramWebApp()?.initData) return scheme;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [choice, setChoiceState] = useState<ThemeChoice>(readChoice);
  const [system, setSystem] = useState<Resolved>(systemScheme);

  useEffect(() => {
    const refresh = () => setSystem(systemScheme());
    const media = window.matchMedia('(prefers-color-scheme: dark)');
    media.addEventListener('change', refresh);
    getTelegramWebApp()?.onEvent?.('themeChanged', refresh);
    return () => {
      media.removeEventListener('change', refresh);
      getTelegramWebApp()?.offEvent?.('themeChanged', refresh);
    };
  }, []);

  const resolved = choice === 'system' ? system : choice;

  useEffect(() => {
    document.documentElement.dataset.theme = resolved;
    paintChrome(CHROME[resolved]);
  }, [resolved]);

  const setChoice = useCallback((next: ThemeChoice) => {
    setChoiceState(next);
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch {
      return;
    }
  }, []);

  const value = useMemo(() => ({ choice, resolved, setChoice }), [choice, resolved, setChoice]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const value = useContext(ThemeContext);
  if (!value) throw new Error('useTheme must be used inside ThemeProvider');
  return value;
}
