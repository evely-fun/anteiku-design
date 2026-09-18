import { useState } from 'react';
import { api } from '../api/calls';
import { describeError, errorCode } from '../api/client';
import type { Toggle } from '../api/types';
import { useNavigation } from '../app/navigation';
import { useProfile } from '../app/profile';
import { useTheme, type ThemeChoice } from '../app/theme';
import { useToast } from '../app/toast';
import { useT } from '../i18n';
import type { StringKey } from '../i18n/strings';
import { getTelegramWebApp, openLink, openTelegramLink, triggerNotificationHaptic } from '../telegram/telegram';
import { Action, Group, Row, Segmented, Sheet, Switch, TabTitle } from '../ui/kit';
import type { MarkName } from '../ui/marks';

const TOGGLES: { key: Toggle; title: StringKey; note: StringKey; mark: MarkName; inverted?: boolean }[] = [
  { key: 'paused', title: 'settings.receive', note: 'settings.receive.note', mark: 'mail', inverted: true },
  { key: 'accept_media', title: 'settings.media', note: 'settings.media.note', mark: 'bubbles' },
  { key: 'accept_links', title: 'settings.links', note: 'settings.links.note', mark: 'link' },
  { key: 'soft_filter', title: 'settings.filter', note: 'settings.filter.note', mark: 'shield' },
  { key: 'silent', title: 'settings.silent', note: 'settings.silent.note', mark: 'clock' },
];

type Editor = 'nick' | 'prompt' | 'reset' | 'erase' | null;

export function SettingsScreen() {
  const { profile, save, replace } = useProfile();
  const { choice, setChoice } = useTheme();
  const { open } = useNavigation();
  const notify = useToast();
  const { lang, t } = useT();
  const [editor, setEditor] = useState<Editor>(null);
  const [value, setValue] = useState('');
  const [busy, setBusy] = useState(false);
  const [problem, setProblem] = useState('');

  if (!profile) {
    return (
      <div className="px-4 pt-6">
        <div className="skeleton h-8 w-40 rounded-xl" />
        <div className="skeleton mt-6 h-[180px] rounded-[22px]" />
        <div className="skeleton mt-4 h-[300px] rounded-[22px]" />
      </div>
    );
  }

  const toggle = async (key: Toggle, next: boolean) => {
    try {
      await save({ [key]: next });
    } catch (cause) {
      notify(describeError(cause), 'danger');
    }
  };

  const edit = (target: Editor) => {
    setProblem('');
    setValue(target === 'nick' ? profile.nick ?? '' : target === 'prompt' ? profile.prompt : '');
    setEditor(target);
  };

  const submit = async () => {
    setBusy(true);
    setProblem('');
    try {
      if (editor === 'nick') replace(await api.nick(value));
      if (editor === 'prompt') await save({ prompt: value });
      if (editor === 'reset') replace(await api.reset());
      if (editor === 'erase') {
        await api.erase();
        getTelegramWebApp()?.close();
        return;
      }
      triggerNotificationHaptic('success');
      notify(editor === 'reset' ? t('settings.reset.done') : t('common.saved'), 'success');
      setEditor(null);
    } catch (cause) {
      triggerNotificationHaptic('error');
      const code = errorCode(cause);
      setProblem(editor === 'nick' && ['format', 'reserved', 'taken'].includes(code) ? t(`nick.${code}` as StringKey) : describeError(cause));
    } finally {
      setBusy(false);
    }
  };

  const legal = (kind: 'terms' | 'privacy' | 'safety') => openLink(`${window.location.origin}/legal/${kind}-${lang}.html`);

  const support = () => {
    notify(t('settings.support.toast'));
    openTelegramLink(`https://t.me/${profile.bot}`);
  };

  const exportData = async () => {
    try {
      await api.exportData();
      triggerNotificationHaptic('success');
      notify(t('settings.export.done'), 'success');
    } catch (cause) {
      notify(describeError(cause), 'danger');
    }
  };

  return (
    <div className="grid gap-5 pb-6">
      <TabTitle title={t('settings.title')} />

      {profile.role && (
        <Group>
          <Row mark="shield" title={t('admin.title')} note={profile.role === 'owner' ? t('admin.role.owner') : t('admin.role.admin')} onClick={() => open('admin')} />
        </Group>
      )}

      <Group title={t('settings.group.link')}>
        <Row mark="key" title={t('settings.nick')} note={profile.nick ? `@${profile.nick}` : t('settings.nick.none')} onClick={() => edit('nick')} />
        <Row mark="bubbles" title={t('settings.prompt')} note={profile.prompt || t('settings.prompt.none')} onClick={() => edit('prompt')} />
        <Row mark="spark" title={t('settings.reset')} note={t('settings.reset.note')} onClick={() => edit('reset')} />
      </Group>

      <Group title={t('settings.group.messages')} footer={t('settings.promise')}>
        {TOGGLES.map((item) => {
          const raw = profile.settings[item.key];
          const checked = item.inverted ? !raw : raw;
          return (
            <Row key={item.key} mark={item.mark} title={t(item.title)} note={t(item.note)}>
              <Switch checked={checked} label={t(item.title)} onChange={(next) => toggle(item.key, item.inverted ? !next : next)} />
            </Row>
          );
        })}
      </Group>

      <Group title={t('settings.group.app')}>
        <div className="px-4 py-3.5">
          <p className="pb-2 text-[13px] font-semibold text-ink-soft">{t('settings.language')}</p>
          <Segmented
            id="lang"
            value={profile.lang}
            onChange={(next) => save({ lang: next }).catch(() => undefined)}
            options={[
              { value: 'ru', label: 'Русский' },
              { value: 'en', label: 'English' },
            ]}
          />
        </div>
        <div className="px-4 py-3.5">
          <p className="pb-2 text-[13px] font-semibold text-ink-soft">{t('settings.theme')}</p>
          <Segmented<ThemeChoice>
            id="theme"
            value={choice}
            onChange={setChoice}
            options={[
              { value: 'system', label: t('settings.theme.system') },
              { value: 'light', label: t('settings.theme.light') },
              { value: 'dark', label: t('settings.theme.dark') },
            ]}
          />
        </div>
      </Group>

      <Group>
        <Row mark="crown" title={profile.premium ? t('settings.premium.active') : t('settings.premium')} onClick={() => open('premium')} />
        <Row mark="bubbles" title={t('settings.support')} note={t('settings.support.note')} onClick={support} />
      </Group>

      <Group title={t('settings.group.data')}>
        <Row mark="key" title={t('settings.export')} note={t('settings.export.note')} onClick={exportData} />
        <Row mark="ban" title={t('settings.erase')} note={t('settings.erase.note')} onClick={() => edit('erase')} />
        <Row mark="lock" title={t('settings.privacy')} onClick={() => legal('privacy')} />
        <Row mark="flag" title={t('settings.terms')} onClick={() => legal('terms')} />
        <Row mark="shield" title={t('settings.safety')} onClick={() => legal('safety')} />
      </Group>

      <p className="px-8 text-center text-[12px] text-ink-faint">{profile.id}</p>

      <Sheet open={editor !== null} onClose={() => setEditor(null)} title={editor ? t(`settings.${editor}.title` as StringKey) : ''}>
        <div className="grid gap-3 px-5 pb-5">
          {editor === 'reset' || editor === 'erase' ? (
            <p className="text-[14.5px] leading-snug text-ink-soft">{t(editor === 'reset' ? 'settings.reset.confirm' : 'settings.erase.confirm')}</p>
          ) : (
            <>
              <p className="text-[13.5px] leading-snug text-ink-soft">
                {editor === 'nick' ? t('settings.nick.hint', { bot: profile.bot }) : t('settings.prompt.hint')}
              </p>
              <div className="rounded-[16px] bg-well px-4 py-3">
                {editor === 'nick' ? (
                  <input
                    autoFocus
                    value={value}
                    maxLength={24}
                    onChange={(event) => setValue(event.target.value.replace(/[^a-zA-Z0-9_]/g, '').toLowerCase())}
                    placeholder="dima_z"
                    aria-label={t('settings.nick')}
                    className="w-full text-[16px] font-semibold"
                  />
                ) : (
                  <textarea
                    autoFocus
                    value={value}
                    maxLength={140}
                    rows={3}
                    onChange={(event) => setValue(event.target.value)}
                    placeholder={t('settings.prompt.placeholder')}
                    aria-label={t('settings.prompt')}
                    className="w-full text-[16px] leading-snug"
                  />
                )}
              </div>
              {editor === 'prompt' && <p className="text-right text-[12px] text-ink-faint tabular">{value.length}/140</p>}
            </>
          )}
          {problem && <p className="text-[13.5px] font-semibold text-danger">{problem}</p>}
          <Action tone={editor === 'reset' || editor === 'erase' ? 'danger' : 'ink'} busy={busy} onClick={submit} disabled={editor === 'nick' && value.length < 4}>
            {editor === 'reset' ? t('settings.reset.yes') : editor === 'erase' ? t('settings.erase.yes') : t('common.save')}
          </Action>
          {editor === 'prompt' && profile.prompt && (
            <Action tone="soft" onClick={() => { setValue(''); save({ prompt: '' }).then(() => setEditor(null), () => undefined); }}>
              {t('settings.prompt.clear')}
            </Action>
          )}
        </div>
      </Sheet>
    </div>
  );
}
