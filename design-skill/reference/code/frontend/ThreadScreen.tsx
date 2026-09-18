import { m } from 'motion/react';
import { useEffect, useRef, useState } from 'react';
import { api } from '../api/calls';
import { describeError } from '../api/client';
import type { Item, Thread } from '../api/types';
import { useNavigation } from '../app/navigation';
import { useProfile } from '../app/profile';
import { useToast } from '../app/toast';
import { useT } from '../i18n';
import { ago, clock } from '../lib/format';
import { ease, spring } from '../lib/motion';
import { triggerNotificationHaptic } from '../telegram/telegram';
import { MoreGlyph, SendGlyph } from '../ui/icons';
import { Action, EmptyState, PageHeader, Pressable, Row, Sheet, Spinner } from '../ui/kit';
import { kindLabel } from './kinds';

const REACTIONS = ['🔥', '❤', '🤣', '😱'];
const REASONS = ['harm', 'intimate', 'child', 'spam', 'other'] as const;
const URGENT: readonly Reason[] = ['intimate', 'child'];
type Reason = (typeof REASONS)[number];
const shown = (emoji: string) => (emoji === '❤' ? '❤️' : emoji);

export function ThreadScreen() {
  const { param, back } = useNavigation();
  const { reload } = useProfile();
  const notify = useToast();
  const { lang, t } = useT();
  const [thread, setThread] = useState<Thread | null>(null);
  const [failed, setFailed] = useState(false);
  const [draft, setDraft] = useState('');
  const [sending, setSending] = useState(false);
  const [menu, setMenu] = useState(false);
  const [reporting, setReporting] = useState(false);
  const bottom = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!param) return;
    api.thread(param).then((value) => {
      setThread(value);
      reload();
    }, () => setFailed(true));
  }, [param, reload]);

  useEffect(() => {
    bottom.current?.scrollIntoView({ block: 'end' });
  }, [thread?.messages.length]);

  if (failed) {
    return (
      <>
        <PageHeader title={t('thread.title')} />
        <EmptyState mark="flag" title={t('thread.gone.title')} note={t('thread.gone.note')}>
          <Action tone="soft" className="mt-5" onClick={back}>{t('common.back')}</Action>
        </EmptyState>
      </>
    );
  }

  if (!thread) {
    return (
      <>
        <PageHeader title={t('thread.title')} />
        <div className="grid gap-3 px-4 pt-2">
          <div className="skeleton h-24 w-4/5 rounded-[22px]" />
          <div className="skeleton ml-auto h-14 w-3/5 rounded-[22px]" />
        </div>
      </>
    );
  }

  const root = thread.messages[0];
  const owner = thread.role === 'owner';

  const send = async () => {
    const text = draft.trim();
    if (!text || sending) return;
    setSending(true);
    try {
      const item = await api.reply(thread.id, text);
      setThread({ ...thread, messages: [...thread.messages, item] });
      setDraft('');
      triggerNotificationHaptic('success');
    } catch (cause) {
      triggerNotificationHaptic('error');
      notify(describeError(cause), 'danger');
    } finally {
      setSending(false);
    }
  };

  const react = async (emoji: string) => {
    try {
      const result = await api.react(root.id, emoji);
      setThread({ ...thread, messages: thread.messages.map((item) => (item.id === root.id ? { ...item, reaction: result.reaction } : item)) });
      notify(t('thread.reacted'), 'success');
    } catch (cause) {
      notify(describeError(cause), 'danger');
    }
  };

  const toggleBlock = async () => {
    setMenu(false);
    const target = thread.messages.filter((item) => !item.mine).at(-1) ?? root;
    try {
      const result = thread.blocked ? await api.unblock(target.id) : await api.block(target.id);
      setThread({ ...thread, blocked: result.blocked });
      notify(result.blocked ? t('thread.blocked') : t('thread.unblocked'), 'success');
    } catch (cause) {
      notify(describeError(cause), 'danger');
    }
  };

  const report = async (reason: Reason) => {
    setReporting(false);
    const target = thread.messages.filter((item) => !item.mine).at(-1) ?? root;
    try {
      const result = await api.report(target.id, reason);
      if (result.duplicate) {
        notify(t('thread.reportedAlready'));
        return;
      }
      notify(result.removed ? t('thread.reportedRemoved') : t('thread.reported'), 'success');
      if (result.removed) back();
    } catch (cause) {
      notify(describeError(cause), 'danger');
    }
  };

  const hide = async () => {
    setMenu(false);
    try {
      await api.hide(root.id);
      notify(t('thread.hidden'));
      back();
    } catch (cause) {
      notify(describeError(cause), 'danger');
    }
  };

  const canAct = thread.messages.some((item) => !item.mine);

  return (
    <div className="flex min-h-dvh flex-col">
      <PageHeader title={owner ? t('thread.title') : t('thread.titleOut')} note={ago(root.created_at, lang)}>
        {canAct && (
          <Pressable
            pressScale={0.9}
            aria-label={t('thread.menu')}
            onClick={() => setMenu(true)}
            className="absolute right-3 top-[calc(var(--tg-content-safe-area-inset-top,0px)+var(--tg-safe-area-inset-top,0px)+12px)] flex size-10 items-center justify-center rounded-full hover:bg-well"
          >
            <MoreGlyph size={22} />
          </Pressable>
        )}
      </PageHeader>

      <div className="flex-1 px-4 pb-4">
        <div className="grid gap-2">
          {thread.messages.map((item, index) => (
            <Bubble key={item.id} item={item} lang={lang} first={index === 0} t={t} />
          ))}
        </div>

        {owner && !root.reaction && (
          <m.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0, transition: { duration: 0.3, ease: ease.out } }}
            className="mt-3 flex gap-2"
          >
            {REACTIONS.map((emoji) => (
              <Pressable
                key={emoji}
                pressScale={0.88}
                onClick={() => react(emoji)}
                aria-label={t('thread.react', { emoji: shown(emoji) })}
                className="flex h-11 flex-1 items-center justify-center rounded-[14px] bg-card text-[20px] shadow-soft"
              >
                {shown(emoji)}
              </Pressable>
            ))}
          </m.div>
        )}
        <div ref={bottom} />
      </div>

      <div className="sticky bottom-0 z-10 bg-paper px-3 pt-2" style={{ paddingBottom: 'calc(var(--safe-bottom) + 10px)' }}>
        {thread.blocked ? (
          <p className="px-3 py-3 text-center text-[13.5px] text-ink-soft">{t('thread.blockedNote')}</p>
        ) : thread.can_reply ? (
          <div className="flex items-end gap-2 rounded-[22px] bg-card p-1.5 pl-4 shadow-float">
            <textarea
              value={draft}
              onChange={(event) => setDraft(event.target.value.slice(0, 2000))}
              rows={Math.min(5, Math.max(1, draft.split('\n').length))}
              placeholder={owner ? t('thread.placeholder.owner') : t('thread.placeholder.author')}
              aria-label={t('thread.placeholder.owner')}
              className="min-h-[44px] flex-1 py-[11px] text-[15px] leading-snug"
            />
            <m.button
              type="button"
              onClick={send}
              disabled={!draft.trim() || sending}
              whileTap={{ scale: 0.9 }}
              transition={spring.press}
              aria-label={t('thread.send')}
              className="flex size-11 shrink-0 items-center justify-center rounded-[16px] bg-action text-on-action transition-opacity disabled:opacity-35"
            >
              {sending ? <Spinner /> : <SendGlyph size={20} />}
            </m.button>
          </div>
        ) : (
          <p className="px-3 py-3 text-center text-[13.5px] text-ink-soft">{t('thread.waiting')}</p>
        )}
      </div>

      <Sheet open={menu} onClose={() => setMenu(false)} title={t('thread.menu')}>
        <div className="px-4 pb-4">
          <div className="overflow-hidden rounded-[22px] bg-well [&>*+*]:border-t [&>*+*]:border-line">
            <Row mark="ban" title={thread.blocked ? t('thread.unblock') : t('thread.block')} note={thread.blocked ? undefined : t('thread.block.note')} onClick={toggleBlock} />
            <Row mark="flag" title={t('thread.report')} note={t('thread.report.note')} onClick={() => { setMenu(false); setReporting(true); }} />
            {owner && <Row mark="eye" title={t('thread.hide')} note={t('thread.hide.note')} onClick={hide} />}
          </div>
        </div>
      </Sheet>

      <Sheet open={reporting} onClose={() => setReporting(false)} title={t('report.title')}>
        <div className="px-4 pb-4">
          <div className="overflow-hidden rounded-[22px] bg-well [&>*+*]:border-t [&>*+*]:border-line">
            {REASONS.map((reason) => (
              <Row key={reason} title={t(`report.${reason}`)} note={URGENT.includes(reason) ? t('report.urgent.note') : undefined} onClick={() => report(reason)} />
            ))}
          </div>
        </div>
      </Sheet>
    </div>
  );
}

function Bubble({ item, lang, first, t }: { item: Item; lang: 'ru' | 'en'; first: boolean; t: ReturnType<typeof useT>['t'] }) {
  const label = kindLabel(item.kind, t);
  return (
    <m.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0, transition: { duration: 0.3, ease: ease.out } }}
      className={`flex flex-col ${item.mine ? 'items-end' : 'items-start'}`}
    >
      <div
        className={`max-w-[86%] rounded-[22px] px-4 py-3 ${
          item.mine ? 'rounded-br-[8px] bg-action text-on-action' : `rounded-bl-[8px] bg-card shadow-soft ${first ? 'text-[17px]' : ''}`
        }`}
      >
        {item.media && <img src={item.media} alt="" className="mb-2 max-h-[320px] w-full rounded-[16px] object-cover" />}
        {label && !item.media && (
          <span className={`mb-1 block text-[12.5px] font-bold ${item.mine ? 'opacity-70' : 'text-inbox'}`}>
            {label} · {t('thread.inChat')}
          </span>
        )}
        {item.text && <p className="whitespace-pre-wrap text-[15px] leading-snug wrap-anywhere">{item.text}</p>}
      </div>
      <span className="mt-1 px-2 text-[11.5px] text-ink-faint tabular">
        {clock(item.created_at, lang)}
        {item.reaction && ` · ${shown(item.reaction)}`}
      </span>
    </m.div>
  );
}
