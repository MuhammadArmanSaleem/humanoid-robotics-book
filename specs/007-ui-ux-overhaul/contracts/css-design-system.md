# CSS Design System Contract

**Feature**: UI/UX Overhaul  
**Type**: Design System Specification  
**Date**: 2025-12-23

## Overview

This contract defines the CSS design system variables and conventions that must be consistently applied across all components and pages.

## Spacing Scale

All spacing must use these values (no arbitrary spacing):

```css
--spacing-xs: 4px;    /* Tight spacing, inline elements */
--spacing-sm: 8px;    /* Small gaps, form field padding */
--spacing-md: 12px;   /* Medium gaps, component spacing */
--spacing-lg: 16px;   /* Large gaps, section spacing */
--spacing-xl: 24px;   /* Extra large, page sections */
--spacing-2xl: 32px;  /* Maximum spacing, major sections */
```

**Usage**: `padding: var(--spacing-lg); margin: var(--spacing-md);`

## Typography Hierarchy

All text must use these font sizes with clear visual distinction:

```css
--font-size-xs: 0.75rem;   /* Captions, helper text */
--font-size-sm: 0.875rem;   /* Small body text */
--font-size-base: 1rem;     /* Body text (default) */
--font-size-lg: 1.125rem;   /* Large body, emphasis */
--font-size-xl: 1.25rem;    /* H4 headings */
--font-size-2xl: 1.5rem;    /* H3 headings */
--font-size-3xl: 2rem;      /* H2 headings */
--font-size-4xl: 2.5rem;    /* H1 headings */
```

**Usage**: `font-size: var(--font-size-lg);`

## Color Roles

All colors must use these semantic roles (no hard-coded hex values):

```css
/* Light theme */
--color-background: var(--ifm-background-color);
--color-surface: var(--ifm-background-surface-color);
--color-primary: var(--ifm-color-primary);
--color-muted: var(--ifm-color-content-secondary);
--color-danger: #dc3545;
--color-success: #28a745;
--color-border: var(--ifm-color-emphasis-300);

/* Dark theme */
[data-theme='dark'] {
  --color-background: var(--ifm-background-color);
  --color-surface: var(--ifm-background-surface-color);
  --color-primary: var(--ifm-color-primary);
  --color-muted: var(--ifm-color-content-secondary);
  --color-danger: #ff6b6b;
  --color-success: #51cf66;
  --color-border: var(--ifm-color-emphasis-300);
}
```

**Usage**: `background-color: var(--color-surface); color: var(--color-primary);`

## Form Component Styles

All form inputs must follow these styles:

```css
.form-input {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 8px;
  border: 1px solid var(--color-border);
  font-size: var(--font-size-base);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--ifm-color-primary-rgb), 0.1);
}

.form-input.error {
  border-color: var(--color-danger);
}

.form-error {
  color: var(--color-danger);
  font-size: var(--font-size-sm);
  margin-top: var(--spacing-xs);
}
```

## Component Conventions

1. **CSS Modules**: Component-specific styles use CSS modules (`.module.css`)
2. **Global Variables**: Design system variables defined in `src/css/custom.css`
3. **Theme Awareness**: All colors must respect theme (use CSS variables, not hard-coded)
4. **Responsive**: Use media queries for mobile/tablet adjustments
5. **Comments**: Inline comments explain design decisions

## Compliance

All components must:
- ✅ Use spacing scale variables (no arbitrary values)
- ✅ Use typography scale variables (no arbitrary font sizes)
- ✅ Use color role variables (no hard-coded colors)
- ✅ Work in both light and dark themes
- ✅ Be responsive (mobile, tablet, desktop)
- ✅ Have proper focus states
- ✅ Have proper hover states (where applicable)


