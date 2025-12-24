# Research: UI/UX Overhaul

**Feature**: UI/UX Overhaul  
**Date**: 2025-12-23  
**Status**: Complete

## Research Questions & Decisions

### 1. Docusaurus Theming System

**Question**: How does Docusaurus v3 handle theming, CSS variables, and dark mode?

**Research Findings**:
- Docusaurus v3 uses Infima CSS framework (bundled)
- Theme system uses CSS custom properties (CSS variables)
- Dark mode controlled via `[data-theme='dark']` attribute
- Theme toggle uses `useColorMode()` hook from `@docusaurus/theme-common`
- Custom CSS loaded via `customCss` in `docusaurus.config.js`
- CSS variables follow `--ifm-*` naming convention

**Decision**: Use Docusaurus Infima CSS variables and extend with custom variables for design system. Use `useColorMode()` hook for theme toggle functionality.

**Rationale**: Working within Docusaurus ecosystem ensures compatibility and leverages existing infrastructure. Infima provides base variables that can be extended.

**Alternatives Considered**:
- Complete CSS framework replacement (Tailwind, Bootstrap) - Rejected: Too heavy, breaks Docusaurus integration
- Custom CSS-in-JS solution - Rejected: Adds complexity, not needed for static site

---

### 2. Design System Implementation Approach

**Question**: How to implement consistent spacing, typography, and color system within Docusaurus?

**Research Findings**:
- Infima provides base spacing via `--ifm-spacing-*` variables
- Typography uses `--ifm-font-*` variables
- Colors use `--ifm-color-*` variables
- Custom variables can be added to `:root` and `[data-theme='dark']`
- CSS modules available for component-specific styles
- Global styles in `src/css/custom.css`

**Decision**: Extend Infima variables in `custom.css` with design system tokens (spacing scale, typography scale, color roles). Use CSS modules for component-specific overrides.

**Rationale**: Leverages existing Infima foundation while adding custom design tokens. Maintains Docusaurus compatibility and allows component-level customization.

**Alternatives Considered**:
- Complete custom design system - Rejected: Too much work, breaks Docusaurus integration
- No design system - Rejected: Won't achieve consistency goals

---

### 3. Form Styling Approach

**Question**: How to style form inputs with proper validation feedback within Docusaurus?

**Research Findings**:
- Docusaurus doesn't provide form components by default
- Forms are custom React components in `src/pages/`
- CSS modules can be used for component-specific styles
- Validation can be client-side (React state) and server-side (API)
- Error states need visual feedback (colors, borders, messages)

**Decision**: Create styled form components using CSS modules. Use CSS custom properties for form colors (primary, error, success). Implement real-time validation with visual feedback.

**Rationale**: CSS modules provide component isolation while allowing design system variable usage. Real-time validation improves UX without requiring heavy libraries.

**Alternatives Considered**:
- Form library (React Hook Form, Formik) - Rejected: Adds dependency, current forms work
- Inline styles - Rejected: Hard to maintain, doesn't use design system

---

### 4. Navbar Customization

**Question**: How to customize navbar styling and structure within Docusaurus?

**Research Findings**:
- Navbar configured in `docusaurus.config.js` under `themeConfig.navbar`
- Navbar items can be customized (type, position, label)
- Custom navbar items can be added via swizzling
- CSS can target navbar classes (`.navbar`, `.navbar__item`, etc.)
- Theme toggle can be added via `useColorMode()` hook

**Decision**: Customize navbar via config and CSS. Add theme toggle as custom navbar item. Style with CSS targeting Docusaurus navbar classes.

**Rationale**: Works within Docusaurus constraints while achieving desired visual improvements. No need to swizzle navbar component unless necessary.

**Alternatives Considered**:
- Complete navbar swizzling - Rejected: More complex, may break on Docusaurus updates
- Third-party navbar component - Rejected: Breaks Docusaurus integration

---

### 5. Chat Widget Styling and State Management

**Question**: How to style chat widget and manage state persistence across navigation?

**Research Findings**:
- Chat widget is custom React component in `src/components/ChatWidget/`
- State can be persisted in localStorage
- Z-index management needed for overlay behavior
- CSS modules available for component styling
- React state management sufficient for open/closed state

**Decision**: Use CSS modules for chat widget styling. Persist open/closed state in localStorage. Use high z-index for overlay. Implement loading/error states with visual feedback.

**Rationale**: Simple approach that works with existing component structure. localStorage provides persistence without backend changes.

**Alternatives Considered**:
- Context API for global state - Rejected: Overkill for simple open/closed state
- Backend state management - Rejected: Unnecessary, adds complexity

---

### 6. Theme Toggle Implementation

**Question**: How to implement reliable theme toggle that works across all pages?

**Research Findings**:
- Docusaurus provides `useColorMode()` hook from `@docusaurus/theme-common`
- Theme preference stored in localStorage automatically
- Theme applied via `[data-theme='dark']` attribute on `<html>`
- All CSS variables must respect theme (no hard-coded colors)
- Theme toggle button can be added to navbar or custom component

**Decision**: Use `useColorMode()` hook for theme toggle. Ensure all custom CSS uses theme-aware variables. Add toggle button to navbar with proper styling.

**Rationale**: Uses Docusaurus built-in functionality, ensuring reliability and persistence. No custom theme management needed.

**Alternatives Considered**:
- Custom theme management - Rejected: Unnecessary, Docusaurus handles it
- CSS-only theme toggle - Rejected: Doesn't persist preference

---

### 7. Responsive Design Approach

**Question**: How to ensure responsive design works across mobile, tablet, and desktop?

**Research Findings**:
- Docusaurus provides responsive design out of the box
- Infima includes responsive utilities
- CSS media queries can be used for custom breakpoints
- Mobile-first approach recommended
- Navbar has built-in mobile menu

**Decision**: Use Docusaurus responsive features. Add custom media queries for design system spacing/typography adjustments. Test on mobile, tablet, desktop.

**Rationale**: Leverages existing responsive infrastructure. Only need custom adjustments for design system consistency.

**Alternatives Considered**:
- Custom responsive framework - Rejected: Unnecessary, Docusaurus handles it
- No responsive considerations - Rejected: Breaks mobile experience

---

### 8. CSS Organization Strategy

**Question**: How to organize CSS for maintainability and consistency?

**Research Findings**:
- Global styles in `src/css/custom.css`
- Component-specific styles in CSS modules (`.module.css`)
- Design system variables should be global
- Component overrides should be scoped
- Comments help maintainability

**Decision**: 
- Global design system variables in `custom.css`
- Component-specific styles in CSS modules
- Inline comments explaining design decisions
- Consistent naming conventions

**Rationale**: Clear separation between global system and component styles. Maintainable and follows Docusaurus conventions.

**Alternatives Considered**:
- All styles in one file - Rejected: Hard to maintain
- CSS-in-JS - Rejected: Adds complexity, not needed

---

## Summary

All research questions resolved. Implementation approach:
1. Extend Docusaurus Infima CSS variables for design system
2. Use CSS modules for component-specific styles
3. Leverage Docusaurus built-in features (theme toggle, responsive design)
4. Maintain compatibility with Docusaurus v3
5. No heavy dependencies - CSS-only approach

**Ready for Phase 1**: Design & Contracts


