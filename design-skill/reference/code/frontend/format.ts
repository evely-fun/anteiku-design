import { locale, translate } from '../i18n/runtime';
import type { Language } from '../i18n/strings';

export function plural(language: Language, count: number, forms: [string, string, string]): string {
  if (language === 'en') return count === 1 ? forms[0] : forms[1];
  const tail = count % 100;
  if (tail >= 11 && tail <= 14) return forms[2];
  if (count % 10 === 1) return forms[0];
  if (count % 10 >= 2 && count % 10 <= 4) return forms[1];
  return forms[2];
}

export const formatNumber = (value: number, language?: Language) =>
  new Intl.NumberFormat(locale(language)).format(value);

export function ago(iso: string, language: Language): string {
  const moment = new Date(iso).getTime();
  const seconds = Math.max(0, Math.round((Date.now() - moment) / 1000));
  if (seconds < 60) return translate('time.now', undefined, language);
  const minutes = Math.round(seconds / 60);
  if (minutes < 60) return translate('time.minutes', { n: minutes }, language);
  const hours = Math.round(minutes / 60);
  if (hours < 24) return translate('time.hours', { n: hours }, language);
  const date = new Date(moment);
  const sameYear = date.getFullYear() === new Date().getFullYear();
  return date.toLocaleDateString(locale(language), { day: 'numeric', month: 'short', ...(sameYear ? {} : { year: 'numeric' }) });
}

export function clock(iso: string, language: Language): string {
  return new Date(iso).toLocaleTimeString(locale(language), { hour: '2-digit', minute: '2-digit' });
}

export function dayLabel(day: string, language: Language): string {
  return new Date(`${day}T12:00:00`).toLocaleDateString(locale(language), { day: 'numeric', month: 'short' });
}

export function dateLabel(iso: string, language: Language): string {
  return new Date(iso).toLocaleDateString(locale(language), { day: 'numeric', month: 'long', year: 'numeric' });
}
