import { m } from 'motion/react';
import { useT } from '../i18n';
import type { StringKey } from '../i18n/strings';
import { ease, spring } from '../lib/motion';
import { Mark } from '../ui/kit';
import type { MarkName } from '../ui/marks';
import { useNavigation, type Tab } from './navigation';
import { useProfile } from './profile';

const TABS: { id: Tab; key: StringKey; mark: MarkName }[] = [
  { id: 'home', key: 'nav.home', mark: 'link' },
  { id: 'inbox', key: 'nav.inbox', mark: 'mail' },
  { id: 'settings', key: 'nav.settings', mark: 'sliders' },
];

export function BottomNav() {
  const { tab, selectTab } = useNavigation();
  const { profile } = useProfile();
  const { t } = useT();
  const unread = profile?.unread ?? 0;

  return (
    <m.nav
      aria-label={t('nav.sections')}
      initial={{ y: 90, opacity: 0 }}
      animate={{ y: 0, opacity: 1, transition: { duration: 0.42, ease: ease.drawer } }}
      exit={{ y: 90, opacity: 0, transition: { duration: 0.26, ease: ease.out } }}
      className="pointer-events-none fixed inset-x-0 bottom-0 z-40 flex justify-center px-4"
      style={{ paddingBottom: 'calc(var(--safe-bottom) + 12px)' }}
    >
      <div className="pointer-events-auto relative flex h-[66px] items-stretch gap-1 rounded-[26px] bg-card p-1.5 shadow-float">
        {TABS.map((item) => {
          const active = item.id === tab;
          return (
            <button
              key={item.id}
              type="button"
              aria-current={active ? 'page' : undefined}
              onClick={() => selectTab(item.id)}
              className="relative flex w-[92px] flex-col items-center justify-center gap-0.5 rounded-[20px]"
            >
              {active && <m.span layoutId="nav-active" transition={spring.ui} className="absolute inset-0 rounded-[20px] bg-well" />}
              <m.span className="relative" animate={{ scale: active ? 1.08 : 1, y: active ? -1 : 0 }} transition={spring.press}>
                <Mark name={item.mark} size={28} className={`transition-[filter] duration-300 ${active ? '' : 'mark-muted'}`} />
                {item.id === 'inbox' && unread > 0 && (
                  <span className="absolute -right-2 -top-1 flex h-[18px] min-w-[18px] items-center justify-center rounded-full bg-inbox px-1 text-[10.5px] font-bold text-white tabular">
                    {unread > 99 ? '99+' : unread}
                  </span>
                )}
              </m.span>
              <span className={`relative text-[11px] font-bold transition-colors duration-200 ${active ? 'text-ink' : 'text-ink-faint'}`}>
                {t(item.key)}
              </span>
            </button>
          );
        })}
      </div>
    </m.nav>
  );
}
