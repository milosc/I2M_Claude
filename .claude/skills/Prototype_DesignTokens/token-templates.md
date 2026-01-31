# Token Templates

Ready-to-use templates for generating design tokens.

---

## CSS Custom Properties Template

```css
:root {
  /* ===== COLOR PRIMITIVES ===== */
  
  /* Brand */
  --color-brand-50: #f5f3ff;
  --color-brand-100: #ede9fe;
  --color-brand-200: #ddd6fe;
  --color-brand-300: #c4b5fd;
  --color-brand-400: #a78bfa;
  --color-brand-500: #8b5cf6;
  --color-brand-600: #7c3aed;
  --color-brand-700: #6d28d9;
  --color-brand-800: #5b21b6;
  --color-brand-900: #4c1d95;
  
  /* Neutral */
  --color-neutral-0: #ffffff;
  --color-neutral-50: #fafafa;
  --color-neutral-100: #f4f4f5;
  --color-neutral-200: #e4e4e7;
  --color-neutral-300: #d4d4d8;
  --color-neutral-400: #a1a1aa;
  --color-neutral-500: #71717a;
  --color-neutral-600: #52525b;
  --color-neutral-700: #3f3f46;
  --color-neutral-800: #27272a;
  --color-neutral-900: #18181b;
  --color-neutral-1000: #000000;
  
  /* Semantic */
  --color-success-500: #22c55e;
  --color-warning-500: #f59e0b;
  --color-error-500: #ef4444;
  --color-info-500: #3b82f6;
  
  /* ===== SEMANTIC COLORS ===== */
  
  /* Surface */
  --surface-page: var(--color-neutral-50);
  --surface-card: var(--color-neutral-0);
  --surface-elevated: var(--color-neutral-0);
  --surface-inset: var(--color-neutral-100);
  
  /* Text */
  --text-primary: var(--color-neutral-900);
  --text-secondary: var(--color-neutral-500);
  --text-disabled: var(--color-neutral-400);
  --text-inverse: var(--color-neutral-0);
  --text-link: var(--color-brand-600);
  --text-error: var(--color-error-500);
  
  /* Border */
  --border-default: var(--color-neutral-200);
  --border-strong: var(--color-neutral-300);
  --border-focus: var(--color-brand-500);
  --border-error: var(--color-error-500);
  
  /* Interactive */
  --interactive-primary: var(--color-brand-500);
  --interactive-primary-hover: var(--color-brand-600);
  --interactive-primary-active: var(--color-brand-700);
  --interactive-secondary: var(--color-neutral-100);
  --interactive-destructive: var(--color-error-500);
  
  /* ===== TYPOGRAPHY ===== */
  
  /* Families */
  --font-family-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-family-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  
  /* Sizes */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  --font-size-4xl: 2.25rem;
  --font-size-5xl: 3rem;
  
  /* Line Heights */
  --line-height-tight: 1.25;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  
  /* Weights */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  /* ===== SPACING ===== */
  
  --space-0: 0;
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-20: 5rem;
  --space-24: 6rem;
  
  /* ===== BORDERS ===== */
  
  /* Width */
  --border-width-none: 0;
  --border-width-thin: 1px;
  --border-width-medium: 2px;
  --border-width-thick: 4px;
  
  /* Radius */
  --radius-none: 0;
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-full: 9999px;
  
  /* ===== SHADOWS ===== */
  
  --shadow-none: none;
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-focus: 0 0 0 3px rgb(139 92 246 / 0.2);
  
  /* ===== MOTION ===== */
  
  /* Duration */
  --duration-instant: 0ms;
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 500ms;
  
  /* Easing */
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* ===== Z-INDEX ===== */
  
  --z-base: 0;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-overlay: 300;
  --z-modal: 400;
  --z-popover: 500;
  --z-toast: 600;
  --z-tooltip: 700;
}

/* ===== DARK MODE ===== */

@media (prefers-color-scheme: dark) {
  :root {
    /* Surface */
    --surface-page: var(--color-neutral-900);
    --surface-card: var(--color-neutral-800);
    --surface-elevated: var(--color-neutral-700);
    --surface-inset: var(--color-neutral-900);
    
    /* Text */
    --text-primary: var(--color-neutral-50);
    --text-secondary: var(--color-neutral-400);
    --text-disabled: var(--color-neutral-600);
    --text-inverse: var(--color-neutral-900);
    --text-link: var(--color-brand-400);
    
    /* Border */
    --border-default: var(--color-neutral-700);
    --border-strong: var(--color-neutral-600);
  }
}
```

---

## JSON Token Format

```json
{
  "color": {
    "brand": {
      "50": { "value": "#f5f3ff" },
      "500": { "value": "#8b5cf6" },
      "600": { "value": "#7c3aed" }
    },
    "neutral": {
      "0": { "value": "#ffffff" },
      "900": { "value": "#18181b" }
    },
    "semantic": {
      "success": { "value": "#22c55e" },
      "warning": { "value": "#f59e0b" },
      "error": { "value": "#ef4444" },
      "info": { "value": "#3b82f6" }
    }
  },
  "typography": {
    "fontFamily": {
      "sans": { "value": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" },
      "mono": { "value": "ui-monospace, SFMono-Regular, Consolas, monospace" }
    },
    "fontSize": {
      "xs": { "value": "0.75rem" },
      "sm": { "value": "0.875rem" },
      "base": { "value": "1rem" },
      "lg": { "value": "1.125rem" },
      "xl": { "value": "1.25rem" }
    }
  },
  "spacing": {
    "0": { "value": "0" },
    "1": { "value": "0.25rem" },
    "2": { "value": "0.5rem" },
    "4": { "value": "1rem" },
    "6": { "value": "1.5rem" },
    "8": { "value": "2rem" }
  }
}
```

---

## Color Scale Generator

To generate a consistent 10-step color scale from a base color:

```javascript
function generateColorScale(baseHex) {
  // baseHex is typically the 500 value
  return {
    50:  lighten(baseHex, 95),
    100: lighten(baseHex, 85),
    200: lighten(baseHex, 70),
    300: lighten(baseHex, 50),
    400: lighten(baseHex, 25),
    500: baseHex,
    600: darken(baseHex, 15),
    700: darken(baseHex, 30),
    800: darken(baseHex, 45),
    900: darken(baseHex, 60)
  };
}
```

---

## WCAG Contrast Pairs

Pre-validated color combinations:

| Background | Text Color | Ratio | Use For |
|------------|------------|-------|---------|
| neutral.0 | neutral.900 | 21:1 | Primary text on white |
| neutral.0 | neutral.500 | 7:1 | Secondary text on white |
| neutral.50 | neutral.900 | 19.5:1 | Primary text on light bg |
| brand.500 | neutral.0 | 4.5:1+ | Button text |
| error.500 | neutral.0 | 4.5:1+ | Error text on dark |

---

## Tailwind Integration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: 'var(--color-brand-50)',
          500: 'var(--color-brand-500)',
          600: 'var(--color-brand-600)',
        },
        surface: {
          page: 'var(--surface-page)',
          card: 'var(--surface-card)',
        }
      },
      spacing: {
        '4.5': 'var(--space-4)',
        '6': 'var(--space-6)',
      },
      borderRadius: {
        DEFAULT: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
      },
      boxShadow: {
        DEFAULT: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        focus: 'var(--shadow-focus)',
      }
    }
  }
}
```

---

**Template Version**: 1.0
