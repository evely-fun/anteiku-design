import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react';
import { triggerSelectionHaptic } from '../telegram/telegram';

export type Tab = 'home' | 'inbox' | 'settings';
export type Page = 'thread' | 'stats' | 'premium' | 'story' | 'admin' | 'report';

interface Navigation {
  tab: Tab;
  page: Page | null;
  param: string | null;
  selectTab: (tab: Tab) => void;
  open: (page: Page, param?: string) => void;
  back: () => void;
}

const NavigationContext = createContext<Navigation | null>(null);

function initialPage(): Page | null {
  const screen = new URLSearchParams(window.location.search).get('screen');
  return screen === 'story' || screen === 'stats' || screen === 'premium' || screen === 'admin' || screen === 'report' ? screen : null;
}

function initialTab(): Tab {
  const screen = new URLSearchParams(window.location.search).get('screen');
  return screen === 'inbox' || screen === 'settings' ? screen : 'home';
}

export function NavigationProvider({ children }: { children: ReactNode }) {
  const [tab, setTab] = useState<Tab>(initialTab);
  const [page, setPage] = useState<Page | null>(initialPage);
  const [param, setParam] = useState<string | null>(() => new URLSearchParams(window.location.search).get('id'));
  const [origin, setOrigin] = useState<{ page: Page; param: string | null } | null>(null);

  const selectTab = useCallback((next: Tab) => {
    setPage(null);
    setOrigin(null);
    setTab((current) => {
      if (current !== next) triggerSelectionHaptic();
      return next;
    });
    window.scrollTo({ top: 0 });
  }, []);

  const open = useCallback((next: Page, value?: string) => {
    setOrigin(page ? { page, param } : null);
    setPage(next);
    setParam(value ?? null);
    window.scrollTo({ top: 0 });
  }, [page, param]);

  const back = useCallback(() => {
    if (origin) {
      setPage(origin.page);
      setParam(origin.param);
      setOrigin(null);
    } else {
      setPage(null);
      setParam(null);
    }
    window.scrollTo({ top: 0 });
  }, [origin]);

  const value = useMemo(() => ({ tab, page, param, selectTab, open, back }), [tab, page, param, selectTab, open, back]);
  return <NavigationContext.Provider value={value}>{children}</NavigationContext.Provider>;
}

export function useNavigation() {
  const value = useContext(NavigationContext);
  if (!value) throw new Error('useNavigation must be used inside NavigationProvider');
  return value;
}
