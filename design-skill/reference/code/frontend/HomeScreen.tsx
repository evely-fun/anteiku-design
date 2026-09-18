import { m } from 'motion/react';
import mask from '../assets/art/mask.webp';
import inboxArt from '../assets/cards/inbox.webp';
import premiumArt from '../assets/cards/premium.webp';
import statsArt from '../assets/cards/stats.webp';
import storyArt from '../assets/cards/story.webp';
import { useNavigation, type Page, type Tab } from '../app/navigation';
import { useProfile } from '../app/profile';
import { useToast } from '../app/toast';
import { useT } from '../i18n';
import type { StringKey } from '../i18n/strings';
import { formatNumber, plural } from '../lib/format';
import { rise, stagger } from '../lib/motion';
import { copyText, openTelegramLink, triggerNotificationHaptic } from '../telegram/telegram';
import { CopyGlyph, ShareGlyph } from '../ui/icons';
import { Action, Pressable } from '../ui/kit';

interface Card {
  target: { page?: Page; tab?: Tab };
  art: string;
  tint: string;
  title: StringKey;
}

const CARDS: Card[] = [
  { target: { tab: 'inbox' }, art: inboxArt, tint: '#f64b41', title: 'home.card.inbox' },
  { target: { page: 'story' }, art: storyArt, tint: '#8a57f3', title: 'home.card.story' },
  { target: { page: 'stats' }, art: statsArt, tint: '#09ad7c', title: 'home.card.stats' },
];

export function HomeScreen() {
  const { profile } = useProfile();
  const { open, selectTab } = useNavigation();
  const notify = useToast();
  const { lang, t } = useT();

  if (!profile) return <HomeSkeleton />;

  const copy = async () => {
    if (await copyText(profile.link)) {
      triggerNotificationHaptic('success');
      notify(t('link.copied'), 'success');
    }
  };

  const share = () => {
    const url = `https://t.me/share/url?url=${encodeURIComponent(profile.link)}&text=${encodeURIComponent(t('share.text'))}`;
    openTelegramLink(url);
  };

  const unreadNote = profile.unread > 0
    ? t('home.card.inbox.unread', { n: profile.unread, word: plural(lang, profile.unread, [t('word.new1'), t('word.new2'), t('word.new5')]) })
    : t('home.card.inbox.note');

  return (
    <m.div variants={stagger} initial="initial" animate="animate" className="px-4 pb-6">
      <m.header variants={rise} className="px-1 pb-5 pt-6">
        <p className="text-[14px] font-semibold text-ink-soft tabular">
          {t('home.today', {
            visits: `${profile.today.visits} ${plural(lang, profile.today.visits, [t('word.visit1'), t('word.visit2'), t('word.visit5')])}`,
            messages: `${profile.today.messages} ${plural(lang, profile.today.messages, [t('word.message1'), t('word.message2'), t('word.message5')])}`,
          })}
        </p>
        <h1 className="mt-1 text-[28px] font-extrabold leading-[1.1] tracking-[-0.025em]">{t('home.title')}</h1>
      </m.header>

      <m.section variants={rise} className="relative overflow-hidden rounded-[28px] bg-[#1a84f7] p-5 text-white shadow-soft">
        <img src={mask} alt="" width={260} height={206} className="pointer-events-none absolute -right-10 -top-6 w-[190px] rotate-6" />
        <div className="relative max-w-[62%]">
          <p className="text-[13px] font-semibold text-white/80">{profile.prompt ? t('home.prompt.label') : t('home.link.label')}</p>
          <p className="mt-1.5 text-[21px] font-extrabold leading-[1.18] tracking-[-0.015em] wrap-anywhere">
            {profile.prompt || t('home.prompt.fallback')}
          </p>
        </div>
        <Pressable
          pressScale={0.98}
          onClick={copy}
          aria-label={t('link.copy')}
          className="relative mt-5 flex w-full items-center gap-2 rounded-[14px] bg-white/16 px-3.5 py-3 text-left"
        >
          <span className="min-w-0 flex-1 truncate text-[14px] font-semibold">{profile.short_link}</span>
          <CopyGlyph size={18} className="shrink-0 opacity-80" />
        </Pressable>
        <div className="relative mt-3 grid grid-cols-2 gap-2.5">
          <Action tone="paper" onClick={copy}>
            <CopyGlyph size={18} />
            {t('link.copy')}
          </Action>
          <Action onClick={share} className="!bg-white/16 !text-white">
            <ShareGlyph size={18} />
            {t('link.share')}
          </Action>
        </div>
      </m.section>

      <m.div variants={rise} className="mt-3 grid grid-cols-3 gap-2.5">
        {([
          ['home.total.visits', profile.counts.visits],
          ['home.total.messages', profile.counts.messages],
          ['home.total.replies', profile.counts.replies],
        ] as [StringKey, number][]).map(([key, value]) => (
          <div key={key} className="rounded-[20px] bg-card px-3.5 py-3 shadow-soft">
            <p className="text-[22px] font-extrabold leading-none tracking-[-0.02em] tabular">{formatNumber(value, lang)}</p>
            <p className="mt-1.5 text-[12px] font-semibold text-ink-soft">{t(key)}</p>
          </div>
        ))}
      </m.div>

      <div className="mt-3 grid grid-cols-2 gap-3">
        {CARDS.map((card, index) => (
          <m.div key={card.title} variants={rise} className={index === 0 ? 'col-span-2' : ''}>
            <Pressable
              pressScale={0.975}
              onClick={() => (card.target.page ? open(card.target.page) : selectTab(card.target.tab!))}
              className={`relative block w-full overflow-hidden rounded-[28px] text-left text-white shadow-soft ${
                index === 0 ? 'aspect-[16/10]' : 'aspect-[9/10]'
              }`}
              style={{ backgroundColor: card.tint }}
            >
              <img src={card.art} alt="" className="absolute inset-0 size-full object-cover object-right-bottom" />
              <span className="absolute left-4 top-4 right-4">
                <span className="block text-[19px] font-extrabold leading-tight tracking-[-0.015em]">{t(card.title)}</span>
                {index === 0 && (
                  <span className="mt-1 block max-w-[70%] text-[12.5px] font-semibold leading-snug text-white/85">{unreadNote}</span>
                )}
              </span>
            </Pressable>
          </m.div>
        ))}
      </div>

      <m.div variants={rise} className="mt-3">
        <Pressable
          pressScale={0.975}
          onClick={() => open('premium')}
          className="relative block aspect-[16/7] w-full overflow-hidden rounded-[28px] bg-[#f2a31f] text-left shadow-soft"
        >
          <img src={premiumArt} alt="" className="absolute inset-0 size-full object-cover object-right" />
          <span className="absolute left-4 top-4 max-w-[52%]">
            <span className="block text-[19px] font-extrabold leading-tight tracking-[-0.015em] text-[#2a1d05]">
              {profile.premium ? t('home.premium.active') : t('home.premium')}
            </span>
            <span className="mt-1 block text-[12.5px] font-semibold leading-snug text-[#2a1d05]/75">{t('home.premium.note')}</span>
          </span>
        </Pressable>
      </m.div>

      <m.p variants={rise} className="px-6 pt-5 text-center text-[12.5px] leading-snug text-ink-faint">
        {t('home.promise')}
      </m.p>
    </m.div>
  );
}

function HomeSkeleton() {
  return (
    <div className="px-4 pt-6">
      <div className="skeleton h-4 w-40 rounded-full" />
      <div className="skeleton mt-3 h-8 w-56 rounded-xl" />
      <div className="skeleton mt-5 h-[248px] rounded-[28px]" />
      <div className="mt-3 grid grid-cols-3 gap-2.5">
        {[0, 1, 2].map((key) => <div key={key} className="skeleton h-[70px] rounded-[20px]" />)}
      </div>
      <div className="skeleton mt-3 aspect-[16/10] rounded-[28px]" />
    </div>
  );
}
