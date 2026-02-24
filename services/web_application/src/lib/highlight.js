/**
 * Highlight utility — renders a fixed-position overlay ring around any element.
 * Escapes overflow:hidden / clip ancestors because it is appended to <body>
 * and uses position:fixed relative to the viewport.
 *
 * Usage from Playwright:
 *   await page.evaluate(sel => window.highlightElement(document.querySelector(sel)), '#btn');
 *   await page.locator('button').evaluate(el => window.highlightElement(el));
 *   await page.evaluate(() => window.removeHighlight());
 */

const OVERLAY_ID = '__highlight_overlay__';
const STYLE_ID   = '__highlight_style__';

const CSS = `
@keyframes __highlight_pulse__ {
  0%, 100% {
    box-shadow:
      0 0 0 2px #3b82f6,
      0 0 6px 2px rgba(59, 130, 246, 0.5);
  }
  50% {
    box-shadow:
      0 0 0 4px rgba(59, 130, 246, 0.85),
      0 0 14px 5px rgba(59, 130, 246, 0.25);
  }
}

#${OVERLAY_ID} {
  position: fixed;
  pointer-events: none;
  z-index: 2147483647;
  border-radius: 4px;
  border: 2px solid #3b82f6;
  box-shadow:
    0 0 0 2px #3b82f6,
    0 0 6px 2px rgba(59, 130, 246, 0.5);
  animation: __highlight_pulse__ 1.4s ease-in-out infinite;
  transition: top 80ms ease, left 80ms ease, width 80ms ease, height 80ms ease;
}
`;

function injectStyle() {
  if (document.getElementById(STYLE_ID)) return;
  const style = document.createElement('style');
  style.id = STYLE_ID;
  style.textContent = CSS;
  document.head.appendChild(style);
}

function getOverlay() {
  let overlay = document.getElementById(OVERLAY_ID);
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = OVERLAY_ID;
    document.body.appendChild(overlay);
  }
  return overlay;
}

/** @param {HTMLElement} overlay @param {Element} target */
function positionOverlay(overlay, target) {
  const GAP = 3; // px gap between element edge and ring
  const rect = target.getBoundingClientRect();
  overlay.style.top    = `${rect.top    - GAP}px`;
  overlay.style.left   = `${rect.left   - GAP}px`;
  overlay.style.width  = `${rect.width  + GAP * 2}px`;
  overlay.style.height = `${rect.height + GAP * 2}px`;
}

// Track active state so we can clean up listeners
/** @type {{ destroy: () => void } | null} */
let _active = null;

/**
 * Highlight a DOM element with a pulsing blue ring overlay.
 * Replaces any existing highlight.
 *
 * @param {Element} el
 * @returns {{ destroy: () => void } | undefined}
 */
export function highlightElement(el) {
  if (!el) return undefined;

  // Clean up any previous highlight first
  removeHighlight();

  injectStyle();
  const overlay = getOverlay();

  positionOverlay(overlay, el);

  // Keep overlay in sync if the element moves / page scrolls
  const observer = new ResizeObserver(() => positionOverlay(overlay, el));
  observer.observe(el);
  observer.observe(document.documentElement);

  const onScroll = () => positionOverlay(overlay, el);
  window.addEventListener('scroll', onScroll, { passive: true, capture: true });

  const destroy = () => {
    observer.disconnect();
    window.removeEventListener('scroll', onScroll, { capture: true });
    overlay.remove();
    _active = null;
  };

  _active = { destroy };
  return { destroy };
}

/**
 * Remove the active highlight overlay, if any.
 */
export function removeHighlight() {
  if (_active) {
    _active.destroy();
  } else {
    // Defensive: remove overlay element directly in case state is out of sync
    document.getElementById(OVERLAY_ID)?.remove();
  }
}

// Expose on window so Playwright (and DevTools console) can call them directly
if (typeof window !== 'undefined') {
  /** @type {any} */ (window).highlightElement = highlightElement;
  /** @type {any} */ (window).removeHighlight  = removeHighlight;
}
