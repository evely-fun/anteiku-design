import { useEffect, useRef } from 'react';

export const useRail = <T extends HTMLElement>() => {
  const ref = useRef<T | null>(null);

  useEffect(() => {
    const node = ref.current;
    if (!node || !window.matchMedia?.('(pointer: fine)').matches) return;

    const scrollable = () => node.scrollWidth > node.clientWidth + 1;

    const onWheel = (event: WheelEvent) => {
      if (!scrollable() || Math.abs(event.deltaX) > Math.abs(event.deltaY)) return;
      const before = node.scrollLeft;
      node.scrollLeft += event.deltaY;
      if (node.scrollLeft !== before) event.preventDefault();
    };

    let dragging = false;
    let moved = false;
    let startX = 0;
    let startLeft = 0;

    const onPointerDown = (event: PointerEvent) => {
      if (event.button !== 0 || event.pointerType !== 'mouse' || !scrollable()) return;
      dragging = true;
      moved = false;
      startX = event.clientX;
      startLeft = node.scrollLeft;
    };

    const onPointerMove = (event: PointerEvent) => {
      if (!dragging) return;
      const delta = event.clientX - startX;
      if (Math.abs(delta) > 4) {
        moved = true;
        node.style.cursor = 'grabbing';
      }
      node.scrollLeft = startLeft - delta;
    };

    const onPointerUp = () => {
      dragging = false;
      node.style.cursor = '';
    };

    const onClick = (event: MouseEvent) => {
      if (!moved) return;
      moved = false;
      event.preventDefault();
      event.stopPropagation();
    };

    node.addEventListener('wheel', onWheel, { passive: false });
    node.addEventListener('pointerdown', onPointerDown);
    node.addEventListener('click', onClick, true);
    window.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerup', onPointerUp);
    return () => {
      node.removeEventListener('wheel', onWheel);
      node.removeEventListener('pointerdown', onPointerDown);
      node.removeEventListener('click', onClick, true);
      window.removeEventListener('pointermove', onPointerMove);
      window.removeEventListener('pointerup', onPointerUp);
    };
  }, []);

  return ref;
};
