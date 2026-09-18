import { m } from 'motion/react';
import { useState } from 'react';
import premiumArt from '../assets/cards/premium.webp';
import { api } from '../api/calls';
import { describeError } from '../api/client';
import { useProfile } from '../app/profile';
import { useToast } from '../app/toast';
import { useT } from '../i18n';
import type { StringKey } from '../i18n/strings';
import { dateLabel } from '../lib/format';
import { rise, spring, stagger } from '../lib/motion';
import { openInvoice, openLink, triggerNotificationHaptic, triggerSelectionHaptic } from '../telegram/telegram';
import { CheckGlyph } from '../ui/icons';
import { Action, Mark, PageHeader } from '../ui/kit';
import type { MarkName } from '../ui/marks';

type Plan = 'month' | 'year';

const PERKS: { mark: MarkName; title: StringKey; note: StringKey }[] = [
  { mark: 'globe', title: 'premium.perk.sources', note: 'premium.perk.sources.note' },
  { mark: 'chart', title: 'premium.perk.stats', note: 'premium.perk.stats.note' },
  { mark: 'palette', title: 'premium.perk.themes', note: 'premium.perk.themes.note' },
  { mark: 'infinity', title: 'premium.perk.history', note: 'premium.perk.history.note' },
];

export function PremiumScreen() {
  const { profile, reload } = useProfile();
  const notify = useToast();
  const { lang, t } = useT();
  const [plan, setPlan] = useState<Plan>('month');
  const [busy, setBusy] = useState(false);

  const buy = async () => {
    setBusy(true);
    try {
      const { link } = await api.invoice(plan);
      const status = await openInvoice(link);
      if (status === 'paid') {
        triggerNotificationHaptic('success');
        notify(t('premium.thanks'), 'success');
        window.setTimeout(reload, 1200);
      }
    } catch (cause) {
      notify(describeError(cause), 'danger');
    } finally {
      setBusy(false);
    }
  };

  const cancel = async () => {
    try {
      const result = await api.cancel();
      notify(result.cancelled ? t('premium.cancelled') : t('premium.nothing'), result.cancelled ? 'success' : 'neutral');
    } catch (cause) {
      notify(describeError(cause), 'danger');
    }
  };

  const prices = profile?.prices ?? { month: 99, year: 690 };
  const plans: { id: Plan; title: StringKey; note: StringKey; stars: number }[] = [
    { id: 'month', title: 'premium.plan.month', note: 'premium.plan.month.note', stars: prices.month },
    { id: 'year', title: 'premium.plan.year', note: 'premium.plan.year.note', stars: prices.year },
  ];

  return (
    <div className="pb-8">
      <PageHeader title={t('premium.title')} />
      <m.div variants={stagger} initial="initial" animate="animate" className="grid gap-4 px-4">
        <m.div variants={rise} className="relative aspect-[16/9] overflow-hidden rounded-[28px] bg-[#f2a31f] shadow-soft">
          <img src={premiumArt} alt="" className="absolute inset-0 size-full object-cover object-right" />
          <p className="absolute left-5 top-5 max-w-[42%] text-[21px] font-extrabold leading-[1.15] tracking-[-0.02em] text-[#2a1d05]">
            {profile?.premium ? t('premium.hero.active') : t('premium.hero')}
          </p>
        </m.div>

        {profile?.premium && profile.premium_until && (
          <m.p variants={rise} className="rounded-[18px] bg-premium-wash px-4 py-3 text-[14px] font-semibold">
            {t('premium.until', { date: dateLabel(profile.premium_until, lang) })}
          </m.p>
        )}

        <m.section variants={rise} className="overflow-hidden rounded-[22px] bg-card shadow-soft [&>*+*]:border-t [&>*+*]:border-line">
          {PERKS.map((perk) => (
            <div key={perk.title} className="flex items-center gap-3.5 px-4 py-3.5">
              <Mark name={perk.mark} size={34} />
              <span className="min-w-0 flex-1">
                <span className="block text-[15px] font-bold leading-tight">{t(perk.title)}</span>
                <span className="mt-0.5 block text-[12.5px] leading-snug text-ink-soft">{t(perk.note)}</span>
              </span>
            </div>
          ))}
        </m.section>

        <m.div variants={rise} role="radiogroup" aria-label={t('premium.plans')} className="grid grid-cols-2 gap-3">
          {plans.map((item) => {
            const selected = plan === item.id;
            return (
              <m.button
                key={item.id}
                type="button"
                role="radio"
                aria-checked={selected}
                whileTap={{ scale: 0.97 }}
                transition={spring.press}
                onClick={() => {
                  triggerSelectionHaptic();
                  setPlan(item.id);
                }}
                className={`relative rounded-[22px] border-2 p-4 text-left transition-colors duration-200 ${
                  selected ? 'border-premium bg-premium-wash' : 'border-transparent bg-card shadow-soft'
                }`}
              >
                <span
                  className={`absolute right-3 top-3 flex size-6 items-center justify-center rounded-full transition-colors duration-200 ${
                    selected ? 'bg-premium text-[#2a1d05]' : 'border-2 border-rim'
                  }`}
                >
                  {selected && <CheckGlyph size={14} strokeWidth={2.6} />}
                </span>
                <span className={`block text-[14px] font-bold ${selected ? 'text-ink' : 'text-ink-soft'}`}>{t(item.title)}</span>
                <span className="mt-1 block text-[24px] font-extrabold tracking-[-0.02em] tabular">{item.stars} ⭐</span>
                <span className="mt-1 block text-[12px] leading-snug text-ink-faint">{t(item.note)}</span>
              </m.button>
            );
          })}
        </m.div>

        <m.div variants={rise}>
          <p className="px-2 pb-3 text-[13px] leading-snug text-ink-soft">
            {t(plan === 'month' ? 'premium.consent.month' : 'premium.consent.year', { stars: plan === 'month' ? prices.month : prices.year })}
          </p>
          <Action className="w-full" busy={busy} onClick={buy}>
            {t(plan === 'month' ? 'premium.agree.month' : 'premium.agree.year', { stars: plan === 'month' ? prices.month : prices.year })}
          </Action>
          <p className="px-3 pt-3 text-center text-[12.5px] leading-snug text-ink-faint">{t('premium.honest')}</p>
          {profile?.premium && (
            <Action tone="soft" className="mt-3 w-full" onClick={cancel}>{t('premium.cancel')}</Action>
          )}
          <div className="flex justify-center gap-4 pt-3 text-[12.5px] font-semibold text-ink-soft">
            <button type="button" onClick={() => openLink(`${window.location.origin}/legal/terms-${lang}.html`)}>{t('settings.terms')}</button>
            <button type="button" onClick={() => openLink(`${window.location.origin}/legal/privacy-${lang}.html`)}>{t('settings.privacy')}</button>
          </div>
        </m.div>
      </m.div>
    </div>
  );
}
