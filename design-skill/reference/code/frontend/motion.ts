import type { Transition, Variants } from 'motion/react';

export const ease = {
  out: [0.23, 1, 0.32, 1] as const,
  drawer: [0.32, 0.72, 0, 1] as const,
};

export const spring = {
  press: { type: 'spring', stiffness: 560, damping: 34, mass: 0.6 } as Transition,
  ui: { type: 'spring', stiffness: 340, damping: 32, mass: 0.8 } as Transition,
  soft: { type: 'spring', stiffness: 220, damping: 28 } as Transition,
};

export const rise: Variants = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.42, ease: ease.out } },
};

export const stagger: Variants = {
  initial: {},
  animate: { transition: { staggerChildren: 0.045, delayChildren: 0.02 } },
};

export const tabScreen: Variants = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.3, ease: ease.out } },
  exit: { opacity: 0, transition: { duration: 0.14, ease: ease.out } },
};

export const pushScreen: Variants = {
  initial: { opacity: 0, x: 28 },
  animate: { opacity: 1, x: 0, transition: { duration: 0.38, ease: ease.drawer } },
  exit: { opacity: 0, x: 28, transition: { duration: 0.22, ease: ease.out } },
};

export const sheetPanel: Variants = {
  initial: { y: '100%' },
  animate: { y: 0, transition: { duration: 0.46, ease: ease.drawer } },
  exit: { y: '100%', transition: { duration: 0.28, ease: ease.out } },
};

