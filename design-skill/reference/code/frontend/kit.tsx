import { AnimatePresence, m, useDragControls, type HTMLMotionProps } from 'motion/react';
import { useEffect, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { useNavigation } from '../app/navigation';
import { useT } from '../i18n';
import { ease, sheetPanel, spring } from '../lib/motion';
import { nativeBackAvailable, triggerHaptic, triggerSelectionHaptic } from '../telegram/telegram';
import { ChevronLeft, ChevronRight } from './icons';
import { marks, type MarkName } from './marks';
import { useRail } from '../lib/useRail';

export const Mark = ({ name, size = 28, className = '' }: { name: MarkName; size?: number; className?: string }) => (
  <img src={marks[name]} alt="" width={size} height={size} draggable={false} className={`shrink-0 object-contain ${className}`} />
);

type PressableProps = HTMLMotionProps<'button'> & { pressScale?: number; haptic?: boolean };

export const Pressable = ({ pressScale = 0.97, haptic = true, disabled, onPointerDown, type = 'button', ...rest }: PressableProps) => (
  <m.button
    type={type}
    disabled={disabled}
    whileTap={disabled ? undefined : { scale: pressScale }}
    transition={spring.press}
    onPointerDown={(event) => {
      if (haptic && !disabled) triggerHaptic('light');
      onPointerDown?.(event);
    }}
    {...rest}
  />
);

export const Spinner = ({ size = 18, className = '' }: { size?: number; className?: string }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" className={`spin ${className}`} aria-hidden="true">
    <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" strokeOpacity="0.2" strokeWidth="2.4" />
    <path d="M21 12a9 9 0 0 0-9-9" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" />
  </svg>
);

export const TabTitle = ({ title, note, trailing }: { title: string; note?: string; trailing?: ReactNode }) => (
  <header className="flex items-end gap-3 px-5 pb-5 pt-6">
    <div className="min-w-0 flex-1">
      <h1 className="text-[28px] font-extrabold leading-[1.1] tracking-[-0.025em]">{title}</h1>
      {note && <p className="mt-1.5 text-[14px] leading-snug text-ink-soft">{note}</p>}
    </div>
    {trailing}
  </header>
);

export const PageHeader = ({ title, note, children }: { title: string; note?: string; children?: ReactNode }) => {
  const { back } = useNavigation();
  const { t } = useT();
  const inApp = !nativeBackAvailable();

  return (
    <header className="sticky top-0 z-20 bg-paper pt-safe">
      <div className="flex min-h-[64px] items-center gap-2 px-3 py-2">
        {inApp && (
          <Pressable
            pressScale={0.9}
            aria-label={t('common.back')}
            onClick={back}
            className="flex size-10 shrink-0 items-center justify-center rounded-full text-ink transition-colors hover:bg-well"
          >
            <ChevronLeft size={22} />
          </Pressable>
        )}
        <div className={`min-w-0 flex-1 ${inApp ? '' : 'pl-2'}`}>
          <h1 className="truncate text-[20px] font-extrabold tracking-[-0.02em]">{title}</h1>
          {note && <p className="truncate text-[12.5px] text-ink-soft">{note}</p>}
        </div>
      </div>
      {children}
    </header>
  );
};

export const Sheet = ({
  open,
  onClose,
  title,
  children,
  label,
}: {
  open: boolean;
  onClose: () => void;
  title?: string;
  label?: string;
  children: ReactNode;
}) => {
  const controls = useDragControls();

  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => event.key === 'Escape' && onClose();
    const overflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    window.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = overflow;
      window.removeEventListener('keydown', onKey);
    };
  }, [open, onClose]);

  return createPortal(
    <AnimatePresence>
      {open && (
        <m.div
          key="sheet"
          role="dialog"
          aria-modal="true"
          aria-label={label ?? title}
          className="fixed inset-0 z-50 mx-auto flex max-w-[480px] items-end"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0, transition: { duration: 0.24, ease: ease.out } }}
        >
          <div className="veil absolute inset-0" onClick={onClose} />
          <m.div
            className="relative flex max-h-[92vh] w-full flex-col rounded-t-[28px] bg-card pb-safe shadow-float"
            variants={sheetPanel}
            initial="initial"
            animate="animate"
            exit="exit"
            drag="y"
            dragConstraints={{ top: 0, bottom: 0 }}
            dragElastic={{ top: 0, bottom: 0.5 }}
            dragListener={false}
            dragControls={controls}
            onDragEnd={(_, info) => {
              if (info.offset.y > 110 || info.velocity.y > 640) onClose();
            }}
          >
            <div className="shrink-0 touch-none" onPointerDown={(event) => controls.start(event)}>
              <span className="mx-auto mt-2.5 block h-[5px] w-10 rounded-full bg-rim" />
              {title ? (
                <h2 className="px-5 pb-2 pt-4 text-[20px] font-extrabold tracking-[-0.02em]">{title}</h2>
              ) : (
                <span className="block h-3" />
              )}
            </div>
            <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain">
              {children}
            </div>
          </m.div>
        </m.div>
      )}
    </AnimatePresence>,
    document.body
  );
};

export const Segmented = <T extends string>({
  id,
  value,
  options,
  onChange,
  disabled,
}: {
  id: string;
  value: T;
  options: { value: T; label: string }[];
  onChange: (value: T) => void;
  disabled?: boolean;
}) => (
  <div role="tablist" className="relative flex rounded-[14px] bg-well p-1">
    {options.map((option) => {
      const active = option.value === value;
      return (
        <button
          key={option.value}
          type="button"
          role="tab"
          aria-selected={active}
          disabled={disabled}
          onClick={() => {
            if (active) return;
            triggerSelectionHaptic();
            onChange(option.value);
          }}
          className="relative flex-1 rounded-[10px] px-2 py-2"
        >
          {active && (
            <m.span layoutId={`segment-${id}`} transition={spring.ui} className="absolute inset-0 rounded-[10px] bg-card shadow-soft" />
          )}
          <span className={`relative text-[13.5px] font-bold transition-colors duration-200 ${active ? 'text-ink' : 'text-ink-soft'}`}>
            {option.label}
          </span>
        </button>
      );
    })}
  </div>
);

export const Switch = ({ checked, onChange, label }: { checked: boolean; onChange: (value: boolean) => void; label: string }) => (
  <button
    type="button"
    role="switch"
    aria-checked={checked}
    aria-label={label}
    onClick={() => {
      triggerSelectionHaptic();
      onChange(!checked);
    }}
    className={`flex h-[30px] w-[50px] shrink-0 items-center rounded-full p-[3px] transition-colors duration-300 ${
      checked ? 'justify-end bg-ok' : 'justify-start bg-rim'
    }`}
  >
    <m.span layout transition={spring.press} className="size-6 rounded-full bg-white shadow-soft" />
  </button>
);

export const Group = ({ title, children, footer }: { title?: string; children: ReactNode; footer?: ReactNode }) => (
  <section className="px-4">
    {title && <h2 className="px-1 pb-2 text-[15px] font-bold text-ink-soft">{title}</h2>}
    <div className="overflow-hidden rounded-[22px] bg-card shadow-soft [&>*+*]:border-t [&>*+*]:border-line">{children}</div>
    {footer && <div className="px-1 pt-2 text-[12.5px] leading-snug text-ink-faint">{footer}</div>}
  </section>
);

export const Row = ({
  mark,
  title,
  note,
  value,
  onClick,
  children,
}: {
  mark?: MarkName;
  title: string;
  note?: string;
  value?: ReactNode;
  onClick?: () => void;
  children?: ReactNode;
}) => {
  const body = (
    <>
      {mark && <Mark name={mark} size={30} />}
      <span className="min-w-0 flex-1 text-left">
        <span className="block text-[15px] font-semibold leading-tight">{title}</span>
        {note && <span className="mt-0.5 block text-[12.5px] leading-snug text-ink-soft">{note}</span>}
      </span>
      {value !== undefined && <span className="shrink-0 text-[14px] text-ink-soft tabular">{value}</span>}
      {children}
      {onClick && <ChevronRight size={18} className="shrink-0 text-ink-faint" />}
    </>
  );

  const shape = 'flex w-full items-center gap-3.5 px-4 py-3.5';

  if (!onClick) return <div className={shape}>{body}</div>;

  return (
    <Pressable pressScale={0.985} onClick={onClick} className={`${shape} transition-colors active:bg-well`}>
      {body}
    </Pressable>
  );
};

export const EmptyState = ({ mark, title, note, children }: { mark: MarkName; title: string; note: string; children?: ReactNode }) => (
  <m.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0, transition: { duration: 0.4, ease: ease.out } }}
    className="flex flex-col items-center px-10 py-12 text-center"
  >
    <Mark name={mark} size={88} />
    <h2 className="mt-4 text-[18px] font-extrabold tracking-[-0.015em]">{title}</h2>
    <p className="mt-1.5 max-w-[280px] text-[14px] leading-snug text-ink-soft">{note}</p>
    {children}
  </m.div>
);

type ActionTone = 'ink' | 'soft' | 'danger' | 'paper';

const TONES: Record<ActionTone, string> = {
  ink: 'bg-action text-on-action',
  soft: 'bg-well text-ink',
  danger: 'bg-danger-wash text-danger',
  paper: 'bg-white text-[#1d2030]',
};

export const Action = ({
  tone = 'ink',
  busy,
  disabled,
  className = '',
  children,
  ...rest
}: PressableProps & { tone?: ActionTone; busy?: boolean; children: ReactNode }) => (
  <Pressable
    disabled={disabled || busy}
    className={`flex h-[52px] items-center justify-center gap-2 rounded-[16px] px-5 text-[15px] font-bold transition-opacity disabled:opacity-50 ${TONES[tone]} ${className}`}
    {...rest}
  >
    {busy ? <Spinner /> : children}
  </Pressable>
);

export const Rail = ({ className = '', children }: { className?: string; children: ReactNode }) => {
  const ref = useRail<HTMLDivElement>();
  return (
    <div ref={ref} className={`overflow-x-auto overscroll-x-contain select-none ${className}`}>
      {children}
    </div>
  );
};
