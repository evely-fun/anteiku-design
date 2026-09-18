import { AnimatePresence, domMax, LazyMotion, m, MotionConfig } from 'motion/react';
import { useEffect } from 'react';
import { BottomNav } from './app/BottomNav';
import { NavigationProvider, useNavigation } from './app/navigation';
import { ProfileProvider, useProfile } from './app/profile';
import { ThemeProvider } from './app/theme';
import { ToastProvider } from './app/toast';
import { I18nProvider, useT } from './i18n';
import { pushScreen, tabScreen } from './lib/motion';
import { AdminScreen } from './screens/AdminScreen';
import { HomeScreen } from './screens/HomeScreen';
import { InboxScreen } from './screens/InboxScreen';
import { PremiumScreen } from './screens/PremiumScreen';
import { ReportScreen } from './screens/ReportScreen';
import { SettingsScreen } from './screens/SettingsScreen';
import { StatsScreen } from './screens/StatsScreen';
import { StoryScreen } from './screens/StoryScreen';
import { ThreadScreen } from './screens/ThreadScreen';
import { getTelegramWebApp, isInsideTelegram, nativeBackAvailable, supports } from './telegram/telegram';
import { RetryGlyph } from './ui/icons';
import { Action, EmptyState } from './ui/kit';

const TABS = { home: HomeScreen, inbox: InboxScreen, settings: SettingsScreen };
const PAGES = { thread: ThreadScreen, stats: StatsScreen, premium: PremiumScreen, story: StoryScreen, admin: AdminScreen, report: ReportScreen };

function Shell() {
  const { tab, page, param, back } = useNavigation();
  const { profile, failed, blocked, reload } = useProfile();
  const { t } = useT();
  const Screen = page ? PAGES[page] : TABS[tab];

  useEffect(() => {
    const button = getTelegramWebApp()?.BackButton;
    if (!button || !nativeBackAvailable()) return;
    if (page) {
      button.show();
      button.onClick(back);
    } else {
      button.hide();
    }
    return () => button.offClick(back);
  }, [page, back]);

  if (blocked && !profile) {
    return (
      <div className="mx-auto flex min-h-dvh max-w-[480px] items-center justify-center">
        <EmptyState
          mark="lock"
          title={blocked === 'age_denied' ? t('age.denied.title') : t('age.required.title')}
          note={blocked === 'age_denied' ? t('age.denied.note') : t('age.required.note')}
        >
          {blocked === 'age_required' && (
            <Action tone="soft" className="mt-5" onClick={() => getTelegramWebApp()?.close()}>{t('age.required.action')}</Action>
          )}
        </EmptyState>
      </div>
    );
  }

  if (failed && !profile) {
    return (
      <div className="mx-auto flex min-h-dvh max-w-[480px] items-center justify-center">
        <EmptyState
          mark="mask"
          title={isInsideTelegram() ? t('error.title') : t('error.outside.title')}
          note={isInsideTelegram() ? t('error.offline') : t('error.outside.note')}
        >
          {isInsideTelegram() && (
            <Action tone="soft" className="mt-5" onClick={reload}>
              <RetryGlyph size={18} />
              {t('common.retry')}
            </Action>
          )}
        </EmptyState>
      </div>
    );
  }

  return (
    <div className="mx-auto min-h-dvh max-w-[480px]" style={{ paddingBottom: page ? 'calc(var(--safe-bottom) + 24px)' : 'calc(var(--nav-space) + 20px)' }}>
      <AnimatePresence mode="wait" initial={false}>
        <m.main
          key={page ? `${page}:${param ?? ''}` : tab}
          className={page === 'thread' ? '' : 'pt-safe'}
          variants={page ? pushScreen : tabScreen}
          initial="initial"
          animate="animate"
          exit="exit"
        >
          <Screen />
        </m.main>
      </AnimatePresence>

      <AnimatePresence>
        {!page && (
          <m.span
            key="scrim"
            aria-hidden="true"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="nav-scrim pointer-events-none fixed inset-x-0 bottom-0 z-20"
            style={{ height: 'calc(var(--nav-space) + 36px)' }}
          />
        )}
      </AnimatePresence>

      <AnimatePresence>{!page && <BottomNav key="nav" />}</AnimatePresence>
    </div>
  );
}

export function App() {
  useEffect(() => {
    const app = getTelegramWebApp();
    if (!app) return;
    app.ready();
    app.expand();
    if (supports('7.7')) app.disableVerticalSwipes?.();
  }, []);

  return (
    <LazyMotion features={domMax} strict>
      <MotionConfig reducedMotion="user">
        <ThemeProvider>
          <ToastProvider>
            <ProfileProvider>
              <I18nProvider>
                <NavigationProvider>
                  <Shell />
                </NavigationProvider>
              </I18nProvider>
            </ProfileProvider>
          </ToastProvider>
        </ThemeProvider>
      </MotionConfig>
    </LazyMotion>
  );
}
