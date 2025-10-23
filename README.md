# CRM — Django Customer Relationship Management

This repository contains a full-featured Customer Relationship Management (CRM) web application built with Django. The app provides lead tracking, agent assignment, category-based pipeline management, user authentication, and a modern responsive UI to help small teams manage customers and sales workflows.

## What this project accomplishes

- Streamlines lead and customer tracking with create/read/update/delete (CRUD) operations and category-based organization.
- Supports agent assignment and role-based access so teams can distribute leads and manage responsibilities.
- Provides a responsive UI with consistent styling, intuitive dashboards, and dynamic forms for efficient data entry.
- Secure configuration using environment variables for sensitive settings (e.g., SECRET_KEY) and local .env support.

## Key features

- User authentication and role-based redirects (login, logout, protected views).
- Lead management: create, update, delete, list, and detail views for leads.
- Agent management: create and assign agents to leads, with proper user-agent relationship handling.
- Category management for organizing leads into pipelines or stages.
- Modern UI using Tailwind CSS and crispy forms for improved forms styling and layout.

## Project structure (high level)

- `crm/` — Django project settings, ASGI/WSGI entry points, and environment templates.
- `leads/` — Main app containing models (Lead, Agent, Category, UserProfile), forms, views, and templates for lead workflows.
- `agents/` — App and templates for managing agents (forms and agent-specific views).
- `templates/` — Shared HTML templates (base, navbar, leads, categories, agents, registration).
- `static/` — Static assets (images, CSS overrides) — optional, depending on local setup.
- `env/` — Local Python virtual environment (not committed in most setups).

## Prerequisites

- Python 3.11+ (project uses Python 3.12 in the workspace, 3.11+ recommended)
- pip
- (Optional) virtualenv or venv

## Quick clone & run (local development)

1. Clone the repository:

```bash
git clone https://github.com/gonzalomaartin/CRM.git
cd CRM
git checkout dev
```

2. Create and activate a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy the environment template and set your SECRET_KEY and other env variables:

```bash
cp crm/.template.env crm/.env
# Edit crm/.env and set SECRET_KEY and any database env vars if you use a different DB
```

5. Apply migrations and create a superuser (or use `crm/superuser.txt` if provided):

```bash
python manage.py migrate
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Notes on environment & database

- The project ships configured for SQLite by default for convenience. If you prefer PostgreSQL or another DB, update `crm/settings.py` or set the appropriate environment variables in `crm/.env`.
- Sensitive values (SECRET_KEY, DB credentials) should never be committed. Use the provided `.template.env` as guidance.

## Common troubleshooting

- If you see `django.core.exceptions.ImproperlyConfigured: Set the SECRET_KEY environment variable`, ensure `crm/.env` exists and contains `SECRET_KEY='your-secret'` and that `django-environ` is loading it.
- Favicon and static file not updating? Clear your browser cache or do a hard refresh (Cmd+Shift+R). Browsers cache favicons aggressively.
- If an app name change was performed (e.g., `djcrm` → `crm`) ensure `manage.py`, `crm/wsgi.py`, `crm/asgi.py` and `crm/settings.py` `ROOT_URLCONF` and `WSGI_APPLICATION` settings reference the correct module path.

## What's been implemented (summary of work done)

- Full lead lifecycle (create, view, update, delete) with templated forms and validation.
- Agent one-to-one relationship with User model and custom deletion logic to avoid orphaned users.
- Category list and detail pages with modern styling consistent across the site.
- Environment-driven settings and a switch to SQLite for easier local development when PostgreSQL access is problematic.
- UI improvements using Tailwind CSS and Crispy Forms for better form layout and responsive design.

## Helpful commands

- Run Django checks:
```bash
python manage.py check
```
- Run tests (if any):
```bash
python manage.py test
```

## Next steps & improvements (optional)

- Add automated tests for key workflows (agent assignment, lead CRUD, permissions).
- Add a proper static asset build step (Tailwind CLI or PostCSS) for production-ready styling.
- Add deployment docs (Gunicorn + Nginx, or Docker) and production environment variable examples.

