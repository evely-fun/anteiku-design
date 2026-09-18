import { m } from 'motion/react';
import { useState, type ReactNode } from 'react';
import { ease } from '../lib/motion';
import { translate } from '../i18n/runtime';

const WIDTH = 320;
const HEIGHT = 120;

type Point = { label: string; value: number; hint?: string };

const nice = (value: number) => {
  if (value <= 5) return 5;
  const step = 10 ** Math.floor(Math.log10(value));
  return Math.ceil(value / step) * step;
};

export function Panel({ title, note, children }: { title: string; note?: string; children: ReactNode }) {
  return (
    <section className="rounded-[22px] bg-card p-4 shadow-soft">
      <header className="pb-3">
        <h3 className="text-[14.5px] font-bold">{title}</h3>
        {note && <p className="mt-0.5 text-[12px] text-ink-soft">{note}</p>}
      </header>
      {children}
    </section>
  );
}

function Tooltip({ text }: { text: string }) {
  return (
    <div className="pointer-events-none absolute left-1/2 top-0 -translate-x-1/2 rounded-lg bg-action px-2 py-1 text-[11.5px] font-semibold text-on-action shadow-float">
      {text}
    </div>
  );
}

export function TimeSeries({ points, tone = 'var(--stats)' }: { points: Point[]; tone?: string }) {
  const [active, setActive] = useState<number | null>(null);
  if (points.length < 2) return <Empty />;

  const max = nice(Math.max(...points.map((point) => point.value), 1));
  const step = WIDTH / (points.length - 1);
  const coords = points.map((point, index) => [index * step, HEIGHT - (point.value / max) * (HEIGHT - 12)] as const);
  const line = coords.map(([x, y], index) => `${index ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ');
  const area = `${line} L${WIDTH} ${HEIGHT} L0 ${HEIGHT} Z`;
  const current = active === null ? null : points[active];

  return (
    <div className="relative">
      <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="block w-full" role="img" aria-label={translate('admin.chartLabel')}
        onPointerLeave={() => setActive(null)}
        onPointerMove={(event) => {
          const box = event.currentTarget.getBoundingClientRect();
          const ratio = (event.clientX - box.left) / box.width;
          setActive(Math.max(0, Math.min(points.length - 1, Math.round(ratio * (points.length - 1)))));
        }}
      >
        {[0.25, 0.5, 0.75].map((fraction) => (
          <line key={fraction} x1="0" x2={WIDTH} y1={HEIGHT * fraction} y2={HEIGHT * fraction} stroke="var(--line)" strokeWidth="1" />
        ))}
        <m.path d={area} fill={tone} opacity={0.14} initial={{ opacity: 0 }} animate={{ opacity: 0.14 }} />
        <m.path
          d={line} fill="none" stroke={tone} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
          initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 0.7, ease: ease.out }}
        />
        {active !== null && (
          <g>
            <line x1={coords[active][0]} x2={coords[active][0]} y1="0" y2={HEIGHT} stroke="var(--ink-faint)" strokeWidth="1" strokeDasharray="3 3" />
            <circle cx={coords[active][0]} cy={coords[active][1]} r="4.5" fill={tone} stroke="var(--card)" strokeWidth="2" />
          </g>
        )}
      </svg>
      <div className="flex justify-between pt-2 text-[11px] text-ink-faint tabular">
        <span>{points[0].label}</span>
        <span>{points[points.length - 1].label}</span>
      </div>
      {current && <Tooltip text={`${current.label} · ${current.hint ?? current.value}`} />}
      <span className="absolute right-0 top-0 text-[11px] font-semibold text-ink-faint tabular">{max}</span>
    </div>
  );
}

export function Bars({ points, tone = 'var(--stats)' }: { points: Point[]; tone?: string }) {
  const [active, setActive] = useState<number | null>(null);
  if (!points.length) return <Empty />;
  const max = Math.max(...points.map((point) => point.value), 1);
  const current = active === null ? null : points[active];

  return (
    <div className="relative">
      <div className="flex h-[104px] items-end gap-[2px]">
        {points.map((point, index) => (
          <button
            key={`${point.label}-${index}`}
            type="button"
            aria-label={`${point.label}: ${point.value}`}
            onPointerEnter={() => setActive(index)}
            onPointerLeave={() => setActive(null)}
            onClick={() => setActive(index)}
            className="group flex h-full flex-1 items-end"
          >
            <m.span
              className="block w-full rounded-t-[4px]"
              style={{ backgroundColor: tone, opacity: active === null || active === index ? 1 : 0.45 }}
              initial={{ height: 2 }}
              animate={{ height: `${Math.max(2, (point.value / max) * 100)}%` }}
              transition={{ duration: 0.5, ease: ease.out, delay: Math.min(index, 12) * 0.012 }}
            />
          </button>
        ))}
      </div>
      <div className="flex justify-between pt-2 text-[11px] text-ink-faint tabular">
        <span>{points[0].label}</span>
        <span>{points[Math.floor(points.length / 2)].label}</span>
        <span>{points[points.length - 1].label}</span>
      </div>
      {current && <Tooltip text={`${current.label} · ${current.hint ?? current.value}`} />}
    </div>
  );
}

export function Rows({ points, tone = 'var(--stats)' }: { points: Point[]; tone?: string }) {
  if (!points.length) return <Empty />;
  const max = Math.max(...points.map((point) => point.value), 1);
  return (
    <div className="space-y-2">
      {points.map((point, index) => (
        <div key={`${point.label}-${index}`} className="flex items-center gap-3">
          <span className="w-[86px] shrink-0 truncate text-[12.5px] font-semibold">{point.label}</span>
          <span className="h-[18px] flex-1 overflow-hidden rounded-[6px] bg-well">
            <m.span
              className="block h-full rounded-[6px]"
              style={{ backgroundColor: tone, opacity: 1 - index * 0.07 }}
              initial={{ width: 0 }}
              animate={{ width: `${Math.max(3, (point.value / max) * 100)}%` }}
              transition={{ duration: 0.5, ease: ease.out, delay: index * 0.04 }}
            />
          </span>
          <span className="w-[52px] shrink-0 text-right text-[12.5px] font-bold tabular">{point.hint ?? point.value}</span>
        </div>
      ))}
    </div>
  );
}

const WEEKDAY_KEYS = ['weekday.0', 'weekday.1', 'weekday.2', 'weekday.3', 'weekday.4', 'weekday.5', 'weekday.6'] as const;

export function Heat({ grid }: { grid: number[][] }) {
  const [active, setActive] = useState<string | null>(null);
  const max = Math.max(...grid.flat(), 1);
  const day = (weekday: number) => translate(WEEKDAY_KEYS[weekday] ?? 'weekday.0');
  return (
    <div className="relative">
      <div className="space-y-[3px]">
        {grid.map((row, weekday) => (
          <div key={weekday} className="flex items-center gap-[3px]">
            <span className="w-6 shrink-0 text-[10.5px] font-semibold text-ink-faint">{day(weekday)}</span>
            {row.map((value, hour) => (
              <button
                key={hour}
                type="button"
                aria-label={`${day(weekday)} ${hour}:00, ${value}`}
                onPointerEnter={() => setActive(`${day(weekday)} ${String(hour).padStart(2, '0')}:00 · ${value}`)}
                onPointerLeave={() => setActive(null)}
                onClick={() => setActive(`${day(weekday)} ${String(hour).padStart(2, '0')}:00 · ${value}`)}
                className="h-[14px] flex-1 rounded-[3px]"
                style={{
                  backgroundColor: value ? 'var(--stats)' : 'var(--well)',
                  opacity: value ? 0.25 + (value / max) * 0.75 : 1,
                }}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="flex justify-between pl-8 pt-2 text-[10.5px] text-ink-faint tabular">
        <span>00</span>
        <span>06</span>
        <span>12</span>
        <span>18</span>
        <span>23</span>
      </div>
      {active && <Tooltip text={active} />}
    </div>
  );
}

function Empty() {
  return <p className="py-6 text-center text-[12.5px] text-ink-faint">{translate('admin.empty')}</p>;
}
