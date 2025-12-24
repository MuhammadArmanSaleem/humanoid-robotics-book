# Data Model: UI/UX Overhaul

**Feature**: UI/UX Overhaul  
**Date**: 2025-12-23  
**Status**: Design Phase

## Overview

This feature involves frontend UI/UX improvements only. No backend data model changes are required. However, client-side state management and browser storage are used for theme preferences and chat widget state.

## Client-Side State Entities

### Theme Preference

**Purpose**: Store user's theme preference (light/dark mode) persistently across sessions.

**Storage**: Browser `localStorage`  
**Key**: `theme-preference` (managed by Docusaurus `useColorMode()` hook)

**Attributes**:
- `value`: String - Either `"light"` or `"dark"`
- `persisted`: Boolean - Whether preference is stored (implicit, managed by Docusaurus)

**State Transitions**:
- Initial load: Read from localStorage or use system preference
- User toggles theme: Update value and persist to localStorage
- Page navigation: Value persists (Docusaurus handles)

**Validation Rules**:
- Value must be `"light"` or `"dark"`
- Falls back to system preference if invalid

---

### Form Validation State

**Purpose**: Track validation status of form fields for immediate feedback.

**Storage**: React component state (in-memory, not persisted)

**Attributes** (per form field):
- `value`: String - Current input value
- `touched`: Boolean - Whether field has been interacted with
- `valid`: Boolean - Whether field passes validation
- `error`: String - Error message to display (empty if valid)

**State Transitions**:
- Initial: `{ value: "", touched: false, valid: true, error: "" }`
- User types: Update `value`, validate, set `valid` and `error`
- User blurs field: Set `touched: true`, validate if not already
- Form submission: Validate all fields, show errors for invalid fields

**Validation Rules** (from spec):
- Email: Must match email format regex
- Password: Minimum 6 characters (signin), strength requirements (signup)
- Confirm Password: Must match password field

---

### Chat Widget State

**Purpose**: Track chat widget open/closed state and persist across navigation.

**Storage**: Browser `localStorage` for persistence, React state for UI

**Attributes**:
- `isOpen`: Boolean - Whether chat window is visible
- `persisted`: Boolean - Whether state is stored in localStorage

**Storage Key**: `chat-widget-state`

**State Transitions**:
- Initial load: Read from localStorage or default to `false`
- User opens chat: Set `isOpen: true`, persist to localStorage
- User closes chat: Set `isOpen: false`, persist to localStorage
- Page navigation: State persists (read from localStorage on mount)

**Validation Rules**:
- `isOpen` must be boolean
- Falls back to `false` if invalid

---

## CSS Design System Variables

**Purpose**: Define consistent spacing, typography, and colors across the site.

**Storage**: CSS custom properties in `src/css/custom.css`

### Spacing Scale

```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 12px;
--spacing-lg: 16px;
--spacing-xl: 24px;
--spacing-2xl: 32px;
```

### Typography Scale

```css
--font-size-xs: 0.75rem;   /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 2rem;      /* 32px */
```

### Color Roles

```css
/* Light theme */
--color-background: var(--ifm-background-color);
--color-surface: var(--ifm-background-surface-color);
--color-primary: var(--ifm-color-primary);
--color-muted: var(--ifm-color-content-secondary);
--color-danger: #dc3545; /* Error states */

/* Dark theme */
[data-theme='dark'] {
  --color-background: var(--ifm-background-color);
  --color-surface: var(--ifm-background-surface-color);
  --color-primary: var(--ifm-color-primary);
  --color-muted: var(--ifm-color-content-secondary);
  --color-danger: #ff6b6b; /* Lighter for dark mode */
}
```

---

## Relationships

- **Theme Preference** → **CSS Variables**: Theme preference controls which CSS variable values are active
- **Form Validation State** → **Form UI**: Validation state determines visual feedback (error colors, messages)
- **Chat Widget State** → **Chat Widget UI**: State determines visibility and positioning

---

## Notes

- No backend data model changes required
- All state is client-side (React state or browser storage)
- Design system variables are global CSS, not data entities
- State management is simple (no complex state machines needed)


