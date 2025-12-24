# Quickstart: UI/UX Overhaul

**Feature**: UI/UX Overhaul  
**Date**: 2025-12-23

## Overview

This guide provides a quick reference for implementing the UI/UX overhaul. It covers the design system, component styling, and key implementation patterns.

## Design System Setup

### 1. Define Design System Variables

Add to `src/css/custom.css`:

```css
:root {
  /* Spacing Scale */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;
  --spacing-lg: 16px;
  --spacing-xl: 24px;
  --spacing-2xl: 32px;

  /* Typography Scale */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 2rem;

  /* Color Roles */
  --color-background: var(--ifm-background-color);
  --color-surface: var(--ifm-background-surface-color);
  --color-primary: var(--ifm-color-primary);
  --color-muted: var(--ifm-color-content-secondary);
  --color-danger: #dc3545;
  --color-success: #28a745;
  --color-border: var(--ifm-color-emphasis-300);
}

[data-theme='dark'] {
  --color-danger: #ff6b6b;
  --color-success: #51cf66;
}
```

## Component Implementation Patterns

### Form Input Styling

```css
/* In component.module.css */
.input {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 8px;
  border: 1px solid var(--color-border);
  font-size: var(--font-size-base);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--ifm-color-primary-rgb), 0.1);
}

.input.error {
  border-color: var(--color-danger);
}

.errorMessage {
  color: var(--color-danger);
  font-size: var(--font-size-sm);
  margin-top: var(--spacing-xs);
}
```

### Theme Toggle Implementation

```javascript
import { useColorMode } from '@docusaurus/theme-common';

function ThemeToggle() {
  const { colorMode, setColorMode } = useColorMode();
  
  return (
    <button onClick={() => setColorMode(colorMode === 'dark' ? 'light' : 'dark')}>
      {colorMode === 'dark' ? '☀️' : '🌙'}
    </button>
  );
}
```

### Chat Widget State Persistence

```javascript
// On component mount
useEffect(() => {
  const savedState = localStorage.getItem('chat-widget-state');
  if (savedState) {
    setIsOpen(JSON.parse(savedState));
  }
}, []);

// On state change
useEffect(() => {
  localStorage.setItem('chat-widget-state', JSON.stringify(isOpen));
}, [isOpen]);
```

## Key Implementation Checklist

- [ ] Add design system variables to `custom.css`
- [ ] Style form inputs with proper validation states
- [ ] Add theme toggle to navbar
- [ ] Style chat widget with proper z-index
- [ ] Ensure all colors use CSS variables (no hard-coded)
- [ ] Test theme switching on all pages
- [ ] Test responsive design (mobile, tablet, desktop)
- [ ] Verify form validation feedback works
- [ ] Verify chat widget state persists
- [ ] Check all pages for visual consistency

## Testing

1. **Visual Regression**: Compare before/after screenshots
2. **Theme Toggle**: Switch themes on all pages, verify no broken colors
3. **Form Validation**: Test all form fields with invalid input
4. **Chat Widget**: Open/close chat, navigate pages, verify state persists
5. **Responsive**: Test on mobile, tablet, desktop screen sizes

## Common Pitfalls

- ❌ Hard-coded colors that break theme switching
- ❌ Arbitrary spacing values instead of design system
- ❌ Missing focus states on interactive elements
- ❌ Not testing dark mode
- ❌ Forgetting to persist chat widget state

## Resources

- [Docusaurus Theming](https://docusaurus.io/docs/styling-layout)
- [Infima CSS Framework](https://infima.dev/)
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)


