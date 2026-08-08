# Project Memory & AI Agent Context — Business Inspector

> **Last Updated:** August 7, 2026  
> **Status:** Unified Auth Page (Login + Signup with OTP) & Feature Development  
> **Target Audience:** AI Coding Assistants / Agents working on the Business Inspector repository.

---

## 1. Executive Summary & Architecture Overview

**Business Inspector** is an AI-powered customer intelligence and predictive business analytics platform built with Python (Flask backend) and Vanilla HTML/CSS/JavaScript (frontend). The system ingests sales, customer, and transaction datasets to forecast revenue, predict customer churn, segment customer bases (RFM analysis), and output actionable intelligence.

### Technology Stack
- **Backend Framework:** Flask (Modular Blueprint Architecture)
- **Templating Engine:** Jinja2 (`{% extends "base.html" %}`, block inheritance, flash messages)
- **Frontend Architecture:** Vanilla HTML5, CSS3 (Design Tokens, Glassmorphism, Segmented Tabs), Vanilla JavaScript (ES6+)
- **Data & ML Pipelines:** Python, PyTorch, Pandas, Scikit-learn (located in `ml/` & `app/train_model/`)
- **Web Server & Containerization:** Docker, Docker Compose, Gunicorn, Nginx

---

## 2. Directory Structure & Key Components

```
Business_Inspector/
├── app/
│   ├── __init__.py               # Flask app factory, CORS, Blueprint registration
│   ├── config/                   # App configuration settings (Config class)
│   ├── database/                 # Database initialization and connection handlers
│   ├── models/                   # ORM data models (User, Dataset, Inspection, Predictions)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── extensions.py         # Shared imports & Flask extensions
│   │   ├── auth_home.py          # Blueprint: 'home_auth' -> GET / (homepage)
│   │   ├── auth_inspect.py       # Blueprint: 'inspect_auth' -> GET/POST /inspect
│   │   ├── auth_login.py         # Blueprint: 'login_auth' -> GET/POST /login (Unified Auth UI)
│   │   └── fuc_inspect.py        # Inspection utility functions & route handlers
│   ├── static/
│   │   ├── css/
│   │   │   ├── base/             # Common component CSS (footer, flash messages)
│   │   │   ├── homepage.css      # Design system tokens, hero, grid, CTA styles
│   │   │   ├── inspect.css       # Inspection workspace styling
│   │   │   └── login.css        # Glassmorphic Login & Signup unified stylesheet
│   │   ├── js/
│   │   │   ├── homepage.js       # Smooth scroll, nav toggle, scroll reveal
│   │   │   ├── inspect.js        # File upload UI & dataset inspection logic
│   │   │   └── login.js          # Unified Auth UX (Tab switcher, OTP step reveal, client validation)
│   │   ├── images/               # Media & dashboard graphics
│   │   └── videos/               # Hero background video assets
│   └── templates/
│       ├── base.html             # Master HTML layout template
│       └── auth/
│           ├── homepage.html     # Landing page template
│           ├── inspect.html      # Dataset upload & AI inspect dashboard
│           └── login.html        # Unified Authentication (Login + Signup OTP) template
├── datasets/                     # Sample CSV datasets for testing
├── ml/                           # ML models & training scripts
├── project_flow/                 # AI AGENT MEMORY DIRECTORY
│   ├── last_code.md              # Current system state & context memory (THIS FILE)
│   └── ai_memory.md              # Agent memory rules & architectural guidelines
├── run.py                        # Entry point: runs Flask app on local dev server
└── requirements.txt              # Python dependencies
```

---

## 3. Blueprint & Route Registry

| Blueprint Name | File | Endpoint | Method | Template / Action |
| :--- | :--- | :--- | :--- | :--- |
| `home_auth` | `app/routes/auth_home.py` | `/` | GET | `auth/homepage.html` |
| `login_auth` | `app/routes/auth_login.py` | `/login` | GET, POST | `auth/login.html` |
| `inspect_auth` | `app/routes/auth_inspect.py` | `/inspect/<username>` | GET, POST | `auth/inspect.html` |

---

## 4. Unified Auth Architecture (Login + Signup Single Webpage)

### **HTML Template (`app/templates/auth/login.html`)**:
- Segmented mode tab control (`Sign In` vs `Create Account`).
- Overrides `{% block footer %}{% endblock %}` as empty to hide the default site footer on the auth page.
- **Sign In Form (`#login-form`)**:
  - Email/Username field, Password field with reveal toggle, "Remember me" checkbox, "Forgot password?" link.
- **Create Account Form (`#signup-form`)**:
  - Input fields: **Username**, **Email Address**, **Organization / Company**, **Password** (with reveal toggle).
  - Step 1: **"Get OTP Verification Code"** button (`#btn-get-otp`).
  - Step 2 (Revealed on Get OTP click): **6-Digit OTP Input Box** (`#signup-otp`), OTP success badge, **"Resend OTP"** button with 30s countdown timer, and **"Create Account & Complete Registration"** final submit button.
- Jinja flash message alerts & CSRF hidden field support.

### **CSS Stylesheet (`app/static/css/login.css`)**:
- Glassmorphism dark aesthetic (`rgba(22, 28, 24, 0.7)` card background, `#00c853` green accent, `#36B4B6` teal highlights).
- Segmented tab slider styling (`.auth-tabs`, `.auth-tab.active`).
- Step 2 OTP container smooth drop animation (`.otp-container`).
- Fully responsive layout across mobile, tablet, and desktop devices.

### **JavaScript Interactivity (`app/static/js/login.js`)**:
- **Pure Frontend UX (Zero backend fetch/axios calls as requested)**.
- Handles tab mode switching between Login and Signup forms.
- Dual password reveal toggles.
- Client validation on Get OTP click (checks username, email format, organization, password length >= 6).
- Unfolds the 6-digit OTP verification section with a **5-minute (300s) countdown timer** formatted as `MM:SS`.
- Client validation on complete registration submit.
- Ambient particle canvas background loop (`#login-bg-canvas`).

### **Mail Module Setup**:
- Integrated `Flask-Mail` (`mail = Mail(app)`) using configuration from `app/config/config.py` and environment variables in `.env`.
- OTP emails dispatched via SMTP using `send_otp_email(email, otp, username)` in `app/routes/login_signup/signup_otp.py`.

---

## 5. Guidelines for AI Agents Working on This Repository

1. **Memory Preservation**: Always check `project_flow/last_code.md` and `project_flow/ai_memory.md` before making architectural updates or adding new routes/templates.
2. **Frontend Rules**:
   - Maintain vanilla CSS design tokens (`--clr-green`, `--clr-card`, `--clr-border`).
   - Do NOT introduce backend data fetching (`fetch()`, `axios`) in frontend scripts unless explicitly instructed by the user.
   - Always ensure Jinja template inheritance from `base.html` for views under `app/templates/`.
3. **Route & Blueprint Pattern**:
   - When creating a new route module, place it in `app/routes/`, define a `Blueprint`, and register it in `app/__init__.py`.
