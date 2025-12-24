# Implementation Plan: UI/UX Overhaul

**Branch**: `007-ui-ux-overhaul` | **Date**: 2025-12-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-ui-ux-overhaul/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the Physical AI & Humanoid Robotics Textbook frontend from a visually unfinished, inconsistent state to a professional, modern, product-grade UI/UX standard. This involves establishing a consistent design system (spacing, typography, colors), redesigning authentication forms with proper validation feedback, improving navbar clarity and integration, ensuring chatbot widget reliability, and fixing the theme toggle system. All improvements work within Docusaurus v3 theming constraints without breaking existing functionality.

## Technical Context

**Language/Version**: JavaScript/TypeScript (React 18+), CSS3  
**Primary Dependencies**: Docusaurus v3.x, React 18+, Infima CSS Framework (bundled with Docusaurus), @docusaurus/theme-classic  
**Storage**: Browser localStorage (for theme preference and chat widget state)  
**Testing**: Visual regression testing, manual UI testing, browser compatibility testing  
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge) - desktop and mobile responsive  
**Project Type**: Web application (frontend-only improvements, no backend changes)  
**Performance Goals**: Page load times remain under 2 seconds (constitution requirement), theme switching without flicker, form validation feedback under 100ms  
**Constraints**: Must remain compatible with Docusaurus v3, cannot break documentation rendering, must work within Infima CSS framework constraints, no heavy UI libraries, maintainable CSS-only approach preferred  
**Scale/Scope**: All pages and components across the site (home, signin, signup, textbook pages, navbar, chat widget), responsive design for mobile/tablet/desktop

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

✅ **Content-First Development**: UI/UX improvements enhance the learning experience by making the platform more trustworthy and accessible  
✅ **AI-Assisted Spec-Driven Workflow**: Following Spec-Kit Plus methodology with formal specification  
✅ **Progressive Enhancement Architecture**: Building on existing Docusaurus foundation, not replacing it  
✅ **User-Centered Personalization**: Improving user experience through better visual design and interactions  
✅ **Performance & Scalability Standards**: Maintaining <2s page load times, no performance degradation  
✅ **Test-Before-Implement Discipline**: Visual regression testing and manual testing before deployment  
✅ **Documentation as Code**: Creating PHRs and maintaining specification

### Technical Stack Compliance

✅ **Frontend Framework**: Docusaurus v3.x (constitution requirement) - working within existing framework  
✅ **Testing**: Manual UI testing and visual regression (Jest/Playwright available but not required for CSS-only changes)  
✅ **Deployment**: GitHub Pages (constitution requirement) - no changes needed

### Quality Gates Compliance

✅ **Code Quality**: CSS follows Docusaurus conventions, maintainable and readable  
✅ **Educational Quality**: UI improvements enhance trust and accessibility  
✅ **Security Requirements**: No security implications (frontend-only changes)

### Budget Constraints Compliance

✅ **Zero-Cost Architecture**: All improvements use existing Docusaurus/Infima framework, no additional services required

**Constitution Check Result**: ✅ **PASS** - All gates pass. Feature aligns with constitution requirements.

## Project Structure

### Documentation (this feature)

```text
specs/007-ui-ux-overhaul/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── css/
│   └── custom.css                    # Global CSS overrides, design system variables
├── components/
│   ├── ChatWidget/
│   │   ├── ChatWidget.jsx           # Chat widget component (existing, needs styling)
│   │   └── ChatWidget.module.css    # Chat widget styles (new)
│   ├── NavbarAuth/
│   │   ├── NavbarAuth.js            # Auth navbar component (existing, needs styling)
│   │   └── NavbarAuth.module.css    # Navbar auth styles (new)
│   └── TextSelectionHandler/
│       ├── TextSelectionHandler.jsx # Text selection component (existing)
│       └── TextSelectionHandler.module.css # Text selection styles (new)
├── pages/
│   ├── signin.js                    # Sign in page (existing, needs form styling)
│   ├── signup.js                    # Sign up page (existing, needs form styling)
│   └── index.js                     # Home page (existing, may need spacing adjustments)
└── theme/
    ├── Root.jsx                      # Docusaurus root (existing, may need theme toggle fix)
    └── AuthContext.js                # Auth context (existing, no changes needed)
```

**Structure Decision**: Frontend-only improvements using existing Docusaurus structure. CSS modules for component-specific styles, global CSS for design system variables. No new directories needed - work within existing `src/` structure.

## Complexity Tracking

> **No violations identified - all changes are frontend-only CSS and component styling improvements within Docusaurus constraints**
