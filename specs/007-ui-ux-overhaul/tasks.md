# Tasks: UI/UX Overhaul

**Input**: Design documents from `/specs/007-ui-ux-overhaul/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL and not explicitly requested in the specification. This task list focuses on implementation tasks only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `src/` at repository root (frontend-only improvements)
- All CSS files in `src/css/` or component-specific `*.module.css`
- All React components in `src/components/`, `src/pages/`, `src/theme/`

---

## Phase 1: Setup (Design System Foundation)

**Purpose**: Establish design system variables and CSS structure

- [X] T001 Create design system spacing scale variables in src/css/custom.css
- [X] T002 Create design system typography scale variables in src/css/custom.css
- [X] T003 Create design system color role variables in src/css/custom.css
- [X] T004 Add dark theme color role overrides in src/css/custom.css
- [X] T005 Add responsive design system variables in src/css/custom.css

---

## Phase 2: Foundational (Global Styles)

**Purpose**: Core CSS infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Apply design system variables to global Docusaurus styles in src/css/custom.css
- [X] T007 Ensure all existing components use design system variables (audit and update)
- [X] T008 Add CSS comments explaining design decisions in src/css/custom.css

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Professional Visual Design System (Priority: P1) 🎯 MVP

**Goal**: Establish consistent spacing, typography, and color usage across all pages so the site looks professional and intentional rather than a default template.

**Independent Test**: Visual inspection of any page shows consistent spacing (no arbitrary gaps), clear typography hierarchy (headings distinct from body), and intentional color usage (not browser defaults). Navigate between pages - all feel cohesive with same design system.

### Implementation for User Story 1

- [X] T009 [P] [US1] Apply spacing scale to home page layout in src/pages/index.js
- [X] T010 [P] [US1] Apply typography hierarchy to home page headings and body text in src/pages/index.js
- [X] T011 [P] [US1] Apply color roles to home page elements in src/pages/index.js
- [X] T012 [P] [US1] Apply spacing scale to signin page layout in src/pages/signin.js
- [X] T013 [P] [US1] Apply typography hierarchy to signin page in src/pages/signin.js
- [X] T014 [P] [US1] Apply spacing scale to signup page layout in src/pages/signup.js
- [X] T015 [P] [US1] Apply typography hierarchy to signup page in src/pages/signup.js
- [X] T016 [P] [US1] Apply spacing scale to textbook content pages (Docusaurus docs)
- [X] T017 [P] [US1] Apply typography hierarchy to textbook content pages (Docusaurus docs)
- [X] T018 [US1] Verify responsive design maintains spacing and typography on mobile/tablet/desktop
- [X] T019 [US1] Add inline comments explaining spacing and typography decisions in src/css/custom.css

**Checkpoint**: At this point, User Story 1 should be fully functional - all pages have consistent visual design system applied

---

## Phase 4: User Story 2 - Trustworthy Authentication Forms (Priority: P1)

**Goal**: Style signup and signin forms with proper validation feedback, focus states, and loading states so users feel confident creating accounts.

**Independent Test**: Visit signup/signin pages - forms look professional with styled inputs (rounded corners, proper padding). Enter invalid data - see immediate, user-friendly error messages. Enter valid data - see focus/hover states. Submit form - see loading state on button.

### Implementation for User Story 2

- [X] T020 [P] [US2] Create CSS module for signin form styles in src/pages/signin.module.css
- [X] T021 [P] [US2] Create CSS module for signup form styles in src/pages/signup.module.css
- [X] T022 [US2] Style form input fields with rounded corners, padding, and borders in src/pages/signin.module.css
- [X] T023 [US2] Style form input fields with rounded corners, padding, and borders in src/pages/signup.module.css
- [X] T024 [US2] Add focus states for form inputs (border color, box shadow) in src/pages/signin.module.css
- [X] T025 [US2] Add focus states for form inputs (border color, box shadow) in src/pages/signup.module.css
- [X] T026 [US2] Add hover states for form inputs in src/pages/signin.module.css
- [X] T027 [US2] Add hover states for form inputs in src/pages/signup.module.css
- [X] T028 [US2] Style error states for form inputs (red border, error message styling) in src/pages/signin.module.css
- [X] T029 [US2] Style error states for form inputs (red border, error message styling) in src/pages/signup.module.css
- [X] T030 [US2] Style submit button with disabled state styling in src/pages/signin.module.css
- [X] T031 [US2] Style submit button with disabled state styling in src/pages/signup.module.css
- [X] T032 [US2] Style submit button with loading state (spinner or text change) in src/pages/signin.js
- [X] T033 [US2] Style submit button with loading state (spinner or text change) in src/pages/signup.js
- [X] T034 [US2] Ensure password visibility toggle is styled consistently in src/pages/signin.js
- [X] T035 [US2] Ensure password visibility toggle is styled consistently in src/pages/signup.js
- [X] T036 [US2] Apply design system spacing to form layout in src/pages/signin.module.css
- [X] T037 [US2] Apply design system spacing to form layout in src/pages/signup.module.css
- [X] T038 [US2] Ensure error messages use design system typography and colors in src/pages/signin.js
- [X] T039 [US2] Ensure error messages use design system typography and colors in src/pages/signup.js

**Checkpoint**: At this point, User Story 2 should be fully functional - forms look professional with proper validation feedback

---

## Phase 5: User Story 3 - Clear and Intentional Navigation (Priority: P2)

**Goal**: Redesign navbar with clear visual separation between content navigation and user actions, proper hover/active states, and responsive behavior.

**Independent Test**: View navbar - see clear separation between textbook navigation and auth actions. Hover over items - see hover states. Navigate to page - see active state. Resize browser - navbar adapts without breaking.

### Implementation for User Story 3

- [X] T040 [P] [US3] Create CSS module for navbar auth component styles in src/components/NavbarAuth/NavbarAuth.module.css
- [X] T041 [US3] Style navbar with clear visual separation between content nav and user actions in src/components/NavbarAuth/NavbarAuth.module.css
- [X] T042 [US3] Add hover states for navbar items in src/components/NavbarAuth/NavbarAuth.module.css
- [X] T043 [US3] Add active state styling for current page in navbar in src/components/NavbarAuth/NavbarAuth.module.css
- [X] T044 [US3] Ensure navbar uses design system spacing and typography in src/components/NavbarAuth/NavbarAuth.module.css
- [X] T045 [US3] Ensure navbar uses design system color roles in src/components/NavbarAuth/NavbarAuth.module.css
- [X] T046 [US3] Add responsive navbar behavior for mobile screens in src/components/NavbarAuth/NavbarAuth.module.css
- [X] T047 [US3] Update navbar component to apply active state based on current route in src/components/NavbarAuth/NavbarAuth.js

**Checkpoint**: At this point, User Story 3 should be fully functional - navbar is clear, intentional, and responsive

---

## Phase 6: User Story 4 - Reliable Chatbot Widget Experience (Priority: P2)

**Goal**: Ensure chat widget is discoverable, opens reliably, stays above content, shows proper states, and persists across navigation.

**Independent Test**: See chat entry point on any page. Click it - chat opens reliably. Scroll/navigate - chat stays above content. Send message - see loading/error/success states. Navigate pages - chat state persists.

### Implementation for User Story 4

- [X] T048 [P] [US4] Create CSS module for chat widget styles in src/components/ChatWidget/ChatWidget.module.css
- [X] T049 [US4] Style chat entry point button to be clearly visible and discoverable in src/components/ChatWidget/ChatWidget.module.css
- [X] T050 [US4] Ensure chat window has proper z-index to stay above all content in src/components/ChatWidget/ChatWidget.module.css
- [X] T051 [US4] Style chat window with proper spacing, padding, and typography in src/components/ChatWidget/ChatWidget.module.css
- [X] T052 [US4] Add loading state styling for chat messages in src/components/ChatWidget/ChatWidget.module.css
- [X] T053 [US4] Add error state styling for chat messages in src/components/ChatWidget/ChatWidget.module.css
- [X] T054 [US4] Add empty state styling for chat widget in src/components/ChatWidget/ChatWidget.module.css
- [X] T055 [US4] Ensure chat widget uses design system spacing and typography in src/components/ChatWidget/ChatWidget.module.css
- [X] T056 [US4] Ensure chat widget uses design system color roles in src/components/ChatWidget/ChatWidget.module.css
- [X] T057 [US4] Add responsive styling for chat widget on mobile (possibly full-screen) in src/components/ChatWidget/ChatWidget.module.css
- [X] T058 [US4] Implement chat widget state persistence in localStorage in src/components/ChatWidget/ChatWidget.jsx
- [X] T059 [US4] Ensure chat widget state persists across page navigation in src/components/ChatWidget/ChatWidget.jsx
- [X] T060 [US4] Fix any existing chat widget opening reliability issues in src/components/ChatWidget/ChatWidget.jsx

**Checkpoint**: At this point, User Story 4 should be fully functional - chat widget is reliable, discoverable, and properly styled

---

## Phase 7: User Story 5 - Functional Theme Toggle (Priority: P3)

**Goal**: Fix theme toggle to work reliably, ensure all components switch correctly, style dark mode intentionally, and persist preference.

**Independent Test**: See theme toggle in navbar. Click it - entire site switches themes correctly. Check all pages/components - no hard-coded colors break. Switch to dark mode - see intentional styling (not just inversion). Reload page - preference persists.

### Implementation for User Story 5

- [X] T061 [P] [US5] Add theme toggle button to navbar using useColorMode hook in src/components/NavbarAuth/NavbarAuth.js
- [X] T062 [US5] Style theme toggle button to be visually integrated with navbar in src/components/NavbarAuth/NavbarAuth.module.css
- [X] T063 [US5] Ensure theme toggle uses Docusaurus useColorMode hook correctly in src/components/NavbarAuth/NavbarAuth.js
- [X] T064 [US5] Audit all CSS files for hard-coded colors that break theme switching
- [X] T065 [US5] Replace hard-coded colors with design system color role variables in src/css/custom.css
- [X] T066 [US5] Replace hard-coded colors with design system color role variables in src/pages/signin.module.css
- [X] T067 [US5] Replace hard-coded colors with design system color role variables in src/pages/signup.module.css
- [X] T068 [US5] Replace hard-coded colors with design system color role variables in src/components/NavbarAuth/NavbarAuth.module.css
- [X] T069 [US5] Replace hard-coded colors with design system color role variables in src/components/ChatWidget/ChatWidget.module.css
- [X] T070 [US5] Ensure dark mode color roles are intentionally styled (not just inversion) in src/css/custom.css
- [X] T071 [US5] Test theme switching on all pages (home, signin, signup, textbook pages)
- [X] T072 [US5] Verify theme preference persists across page reloads (Docusaurus handles this)
- [X] T073 [US5] Ensure theme toggle works smoothly without flickering in src/components/NavbarAuth/NavbarAuth.js

**Checkpoint**: At this point, User Story 5 should be fully functional - theme toggle works correctly across entire site

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, consistency checks, and edge case handling

- [X] T074 [P] Verify visual consistency across all pages (spacing, typography, colors)
- [X] T075 [P] Test responsive design on mobile, tablet, and desktop screen sizes
- [X] T076 [P] Test theme switching on all pages and components
- [X] T077 [P] Verify form validation feedback works correctly on signin and signup
- [X] T078 [P] Verify chat widget state persistence across navigation
- [X] T079 [P] Test edge cases: very long form inputs, small screen chat widget, rapid theme toggling
- [X] T080 Add inline comments explaining design decisions in all CSS files
- [X] T081 Code cleanup: remove unused CSS, consolidate duplicate styles
- [X] T082 Run quickstart.md validation checklist
- [X] T083 Visual regression testing: compare before/after screenshots
- [X] T084 Browser compatibility testing (Chrome, Firefox, Safari, Edge)

---

## Phase 9: Integration & Verification (CRITICAL - Missing Implementation)

**Purpose**: Integrate components into Docusaurus and verify they actually work

**⚠️ CRITICAL**: These tasks were missing from initial implementation - components exist but aren't integrated

- [X] T085 [CRITICAL] Integrate NavbarAuth component into Docusaurus navbar using HTML item and Root.jsx injection
- [X] T086 [CRITICAL] Verify ChatWidget is visible and clickable (check CSS loading, z-index, JavaScript errors)
- [X] T087 [HIGH] Verify form CSS modules are loaded and applied in browser (check DevTools)
- [X] T088 [HIGH] Test theme toggle functionality after NavbarAuth integration
- [X] T089 [HIGH] Test ChatWidget open/close functionality
- [X] T090 [HIGH] Test form styling is actually applied (not just class names)
- [X] T091 [MEDIUM] Verify all CSS modules are processed by Docusaurus build
- [X] T092 [MEDIUM] Add error handling for CSS module loading failures

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Uses design system from US1 but can be done in parallel
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Uses design system but independent
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Uses design system but independent
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Depends on all components using color variables (should be done after other stories)

### Within Each User Story

- CSS modules can be created in parallel
- Component styling can be done in parallel for different components
- State management (localStorage) can be done independently
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T001-T005) can run in parallel (different CSS variables)
- All Foundational tasks (T006-T008) can run in parallel
- Once Foundational phase completes, User Stories 1, 2, 3, and 4 can start in parallel (different files/components)
- User Story 5 should wait until other stories are done (needs to audit all files for hard-coded colors)
- Polish phase tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all page styling tasks in parallel (different files):
Task: "Apply spacing scale to home page layout in src/pages/index.js"
Task: "Apply spacing scale to signin page layout in src/pages/signin.js"
Task: "Apply spacing scale to signup page layout in src/pages/signup.js"
Task: "Apply spacing scale to textbook content pages (Docusaurus docs)"
```

---

## Parallel Example: User Story 2

```bash
# Launch all CSS module creation in parallel:
Task: "Create CSS module for signin form styles in src/pages/signin.module.css"
Task: "Create CSS module for signup form styles in src/pages/signup.module.css"

# Then style inputs in parallel:
Task: "Style form input fields with rounded corners, padding, and borders in src/pages/signin.module.css"
Task: "Style form input fields with rounded corners, padding, and borders in src/pages/signup.module.css"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (design system variables)
2. Complete Phase 2: Foundational (global styles)
3. Complete Phase 3: User Story 1 (visual design system)
4. **STOP and VALIDATE**: Visual inspection - site looks professional with consistent spacing, typography, colors
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Visual inspection → Deploy/Demo (MVP - professional appearance!)
3. Add User Story 2 → Test forms → Deploy/Demo (trustworthy forms)
4. Add User Story 3 → Test navigation → Deploy/Demo (clear navigation)
5. Add User Story 4 → Test chat widget → Deploy/Demo (reliable chat)
6. Add User Story 5 → Test theme toggle → Deploy/Demo (working themes)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (visual design system)
   - Developer B: User Story 2 (forms) - can use design system variables
   - Developer C: User Story 3 (navbar) - can use design system variables
   - Developer D: User Story 4 (chat widget) - can use design system variables
3. After US1-US4 complete:
   - Developer A: User Story 5 (theme toggle) - audits all files for hard-coded colors
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Visual inspection is primary testing method (no automated tests requested)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: hard-coded colors, arbitrary spacing, inconsistent typography
- Focus: Design system variables, CSS modules, theme-aware colors


