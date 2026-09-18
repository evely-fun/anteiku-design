import { AnimatePresence, m } from 'motion/react';
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { ease } from '../lib/motion';

type Tone = 'neutral' | 'danger' | 'success';

interface Toast {
  id: number;
  text: string;
  tone: Tone;
}

type Notify = (text: string, tone?: Tone) => void;

const ToastContext = createContext<Notify | null>(null);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toast, setToast] = useState<Toast | null>(null);
  const counter = useRef(0);
  const timer = useRef<number | undefined>(undefined);

  const notify = useCallback<Notify>((text, tone = 'neutral') => {
    window.clearTimeout(timer.current);
    const id = ++counter.current;
    setToast({ id, text, tone });
    timer.current = window.setTimeout(() => setToast((current) => (current?.id === id ? null : current)), 3200);
  }, []);

  useEffect(() => () => window.clearTimeout(timer.current), []);

  const value = useMemo(() => notify, [notify]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="pointer-events-none fixed inset-x-0 top-0 z-[70] mx-auto flex max-w-[480px] justify-center px-4 pt-safe">
        <AnimatePresence>
          {toast && (
            <m.div
              key={toast.id}
              role="status"
              initial={{ opacity: 0, y: -16, scale: 0.96 }}
              animate={{ opacity: 1, y: 0, scale: 1, transition: { duration: 0.36, ease: ease.out } }}
              exit={{ opacity: 0, y: -10, transition: { duration: 0.2 } }}
              className="pointer-events-auto mt-3 flex max-w-full items-center gap-2.5 rounded-2xl bg-action px-4 py-3 text-[13.5px] font-semibold text-on-action shadow-float"
              onClick={() => setToast(null)}
            >
              {toast.tone !== 'neutral' && (
                <span
                  className={`size-2 shrink-0 rounded-full ${toast.tone === 'danger' ? 'bg-danger' : 'bg-ok'}`}
                />
              )}
              <span className="min-w-0">{toast.text}</span>
            </m.div>
          )}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const value = useContext(ToastContext);
  if (!value) throw new Error('useToast must be used inside ToastProvider');
  return value;
}
