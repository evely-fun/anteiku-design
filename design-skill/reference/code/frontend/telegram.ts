type ImpactStyle = 'light' | 'medium' | 'heavy' | 'rigid' | 'soft';
export type InvoiceStatus = 'paid' | 'cancelled' | 'failed' | 'pending' | 'unsupported';
type NoticeType = 'error' | 'success' | 'warning';

interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
  language_code?: string;
}

interface TelegramWebApp {
  initData?: string;
  initDataUnsafe?: { user?: TelegramUser; start_param?: string };
  colorScheme?: 'light' | 'dark';
  platform?: string;
  ready: () => void;
  expand: () => void;
  close: () => void;
  isVersionAtLeast?: (version: string) => boolean;
  setHeaderColor?: (color: string) => void;
  setBackgroundColor?: (color: string) => void;
  setBottomBarColor?: (color: string) => void;
  disableVerticalSwipes?: () => void;
  openInvoice?: (url: string, callback?: (status: InvoiceStatus) => void) => void;
  openTelegramLink?: (url: string) => void;
  openLink?: (url: string, options?: { try_instant_view?: boolean }) => void;
  shareToStory?: (mediaUrl: string, params?: { text?: string; widget_link?: { url: string; name?: string } }) => void;
  onEvent?: (event: string, handler: () => void) => void;
  offEvent?: (event: string, handler: () => void) => void;
  BackButton?: {
    show: () => void;
    hide: () => void;
    onClick: (handler: () => void) => void;
    offClick: (handler: () => void) => void;
  };
  HapticFeedback?: {
    impactOccurred: (style: ImpactStyle) => void;
    notificationOccurred: (type: NoticeType) => void;
    selectionChanged: () => void;
  };
}

declare global {
  interface Window {
    Telegram?: { WebApp?: TelegramWebApp };
  }
}

const HAPTICS_KEY = 'anonka.haptics';

let hapticsEnabled = readHapticsPreference();

function readHapticsPreference(): boolean {
  try {
    return localStorage.getItem(HAPTICS_KEY) !== 'off';
  } catch {
    return true;
  }
}

export const getTelegramWebApp = (): TelegramWebApp | null => {
  if (typeof window === 'undefined') return null;
  return window.Telegram?.WebApp ?? null;
};

export const isInsideTelegram = () => Boolean(getTelegramWebApp()?.initData);

export const supports = (version: string) =>
  Boolean(getTelegramWebApp()?.isVersionAtLeast?.(version));

export const telegramUser = () => getTelegramWebApp()?.initDataUnsafe?.user ?? null;

export const hapticsOn = () => hapticsEnabled;

export const setHapticsOn = (value: boolean) => {
  hapticsEnabled = value;
  try {
    localStorage.setItem(HAPTICS_KEY, value ? 'on' : 'off');
  } catch {
    return;
  }
};

export const triggerHaptic = (style: ImpactStyle = 'light') => {
  if (hapticsEnabled) getTelegramWebApp()?.HapticFeedback?.impactOccurred(style);
};

export const triggerSelectionHaptic = () => {
  if (hapticsEnabled) getTelegramWebApp()?.HapticFeedback?.selectionChanged();
};

export const triggerNotificationHaptic = (type: NoticeType = 'success') => {
  if (hapticsEnabled) getTelegramWebApp()?.HapticFeedback?.notificationOccurred(type);
};

export const paintChrome = (color: string) => {
  const app = getTelegramWebApp();
  if (!app) return;
  if (supports('6.1')) {
    app.setHeaderColor?.(color);
    app.setBackgroundColor?.(color);
  }
  if (supports('7.10')) app.setBottomBarColor?.(color);
};

export const nativeBackAvailable = () => isInsideTelegram() && supports('6.1');

export const openInvoice = (url: string): Promise<InvoiceStatus> =>
  new Promise((resolve) => {
    const app = getTelegramWebApp();
    if (app?.openInvoice && supports('6.1')) {
      app.openInvoice(url, (status) => resolve(status));
      return;
    }
    window.open(url, '_blank', 'noopener');
    resolve('unsupported');
  });


export const openTelegramLink = (url: string) => {
  const app = getTelegramWebApp();
  if (app?.openTelegramLink && isInsideTelegram()) {
    app.openTelegramLink(url);
    return;
  }
  window.open(url, '_blank', 'noopener');
};

export const openLink = (url: string) => {
  const app = getTelegramWebApp();
  if (app?.openLink && isInsideTelegram()) {
    app.openLink(url);
    return;
  }
  window.open(url, '_blank', 'noopener');
};

export const canShareToStory = () => isInsideTelegram() && supports('7.8') && Boolean(getTelegramWebApp()?.shareToStory);

export const shareToStory = (mediaUrl: string, text: string, link: string, name: string) => {
  const app = getTelegramWebApp();
  if (!app?.shareToStory || !supports('7.8')) return false;
  app.shareToStory(mediaUrl, { text, widget_link: { url: link, name } });
  return true;
};

export const copyText = async (text: string): Promise<boolean> => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    const field = document.createElement('textarea');
    field.value = text;
    field.style.position = 'fixed';
    field.style.opacity = '0';
    document.body.appendChild(field);
    field.select();
    const done = document.execCommand('copy');
    field.remove();
    return done;
  }
};
