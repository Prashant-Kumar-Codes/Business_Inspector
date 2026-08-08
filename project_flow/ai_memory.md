# AI Agent Memory Guide — Business Inspector

## Purpose
This directory (`project_flow/`) serves as the long-term context memory for AI coding agents working on the **Business Inspector** project. Future AI agents must read these memory files to understand the current architecture, coding patterns, active features, and design system without repeating past analysis.

---

## 1. Quick Agent Reference

- **App Initialization:** `app/__init__.py`
- **Entry point:** `run.py`
- **Templates:** `app/templates/` (extends `base.html`)
- **Unified Auth Template:** `app/templates/auth/login.html` (Combines Sign In and Create Account + OTP in a single webpage)
- **Stylesheets:** `app/static/css/login.css` (Design tokens & Auth UI styles)
- **Client Scripts:** `app/static/js/login.js` (Pure frontend mode switcher, OTP reveal flow, client validation)
- **Route Blueprints:** `app/routes/`
- **Memory Documents:** `project_flow/last_code.md` and `project_flow/ai_memory.md`

---

## 2. Unified Auth Page Flow

1. **Sign In Mode (`tab-login`):**
   - Displays email/username & password inputs.
   - Preserves original login functionality and layout.
2. **Create Account Mode (`tab-signup`):**
   - Displays **Username**, **Email Address**, **Organization**, and **Password**.
   - Includes **"Get OTP Verification Code"** button.
   - When clicked, validates input fields, shows loading spinner, and reveals the **6-Digit OTP** input field + **"Resend OTP"** timer + **"Create Account & Complete Registration"** final submit button.
3. **Pure Frontend Execution:**
   - Zero `fetch()` / `axios` backend data fetching calls in JS.
   - Full Jinja template compatibility (`{% extends "base.html" %}`, CSRF inputs, flash alerts).

---

## 3. Memory Protocol for AI Agents

When initiating or concluding any task in this workspace:
1. **Read Context First:** Read `project_flow/last_code.md` to get the latest snapshot of implemented features, active routes, CSS design tokens, and frontend/backend architecture.
2. **Adhere to Principles:**
   - Use Jinja2 templating syntax (`{% extends "base.html" %}`) for view templates.
   - Do NOT implement unrequested backend fetching in pure frontend tasks.
   - Match the dark glassmorphic green/emerald design aesthetic (`#00c853`).
3. **Update Memory Before Finishing:** Update `project_flow/last_code.md` with any newly added components, modified files, routes, or design additions so the next agent has full context.
