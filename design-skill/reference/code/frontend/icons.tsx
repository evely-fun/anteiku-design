import type { ReactNode, SVGProps } from 'react';

type IconProps = { size?: number } & Omit<SVGProps<SVGSVGElement>, 'width' | 'height'>;

const Glyph = ({ size = 20, children, strokeWidth = 1.9, ...rest }: IconProps & { children: ReactNode }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={strokeWidth}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
    {...rest}
  >
    {children}
  </svg>
);

export const ChevronLeft = (props: IconProps) => (
  <Glyph {...props}>
    <path d="m14.5 5.5-6.5 6.5 6.5 6.5" />
  </Glyph>
);

export const ChevronRight = (props: IconProps) => (
  <Glyph {...props}>
    <path d="m9.5 5.5 6.5 6.5-6.5 6.5" />
  </Glyph>
);

export const CopyGlyph = (props: IconProps) => (
  <Glyph {...props}>
    <rect x="8.5" y="8.5" width="11" height="11" rx="3" />
    <path d="M15.5 8.5V7a2.5 2.5 0 0 0-2.5-2.5H7A2.5 2.5 0 0 0 4.5 7v6A2.5 2.5 0 0 0 7 15.5h1.5" />
  </Glyph>
);

export const ShareGlyph = (props: IconProps) => (
  <Glyph {...props}>
    <path d="M12 14.5V4" />
    <path d="m8 8 4-4 4 4" />
    <path d="M6.5 11.5H6A1.5 1.5 0 0 0 4.5 13v5A1.5 1.5 0 0 0 6 19.5h12a1.5 1.5 0 0 0 1.5-1.5v-5a1.5 1.5 0 0 0-1.5-1.5h-.5" />
  </Glyph>
);

export const SendGlyph = (props: IconProps) => (
  <Glyph {...props}>
    <path d="M12 19V5.5" />
    <path d="m6 11.5 6-6 6 6" />
  </Glyph>
);

export const MoreGlyph = (props: IconProps) => (
  <Glyph {...props}>
    <circle cx="5.5" cy="12" r="1" fill="currentColor" />
    <circle cx="12" cy="12" r="1" fill="currentColor" />
    <circle cx="18.5" cy="12" r="1" fill="currentColor" />
  </Glyph>
);

export const CheckGlyph = (props: IconProps) => (
  <Glyph {...props}>
    <path d="m5 12.5 4.5 4.5L19 7.5" />
  </Glyph>
);

export const LockGlyph = (props: IconProps) => (
  <Glyph {...props}>
    <rect x="5.5" y="10.5" width="13" height="9" rx="2.5" />
    <path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5" />
  </Glyph>
);

export const RetryGlyph = (props: IconProps) => (
  <Glyph {...props}>
    <path d="M19.5 12a7.5 7.5 0 1 1-2.2-5.3" />
    <path d="M19.5 4.5v4h-4" />
  </Glyph>
);
