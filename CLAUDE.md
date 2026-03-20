# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based project management system (项目管理系统) built primarily around Django's admin interface. The application provides project management, weekly reports, user management, and property/house management features.

**Tech Stack**: Django 4.2.3, Python 3.8+, SQLite (dev), Docker/Docker Compose for deployment.

## Development Commands

### Package Management (IMPORTANT: Use `uv`)

**This project uses `uv` for dependency management. Always use `uv` instead of `pip`.**

```bash
# Install dependencies
uv pip install <package-name>

# Install from requirements.txt
uv pip install -r requirements.txt

# Create virtual environment with uv
uv venv

# Run commands with uv
uv run python manage.py runserver
```

### Running the Application

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or run locally (requires virtual environment)
python manage.py runserver 0.0.0.0:8200
```

### Database Operations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create superuser in Docker
docker-compose exec web python manage.py createsuperuser
```

### Testing

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test apps.projects
python manage.py test apps.weekly
python manage.py test apps.user
python manage.py test apps.house
python manage.py test apps.core
```

### Other Useful Commands

```bash
# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell

# Check for issues
python manage.py check
```

## Architecture

### Project Structure

```
project-sys/
├── project_sys/          # Main Django project (settings, urls, wsgi)
├── apps/                 # Django applications
│   ├── core/            # Base models and utilities
│   ├── projects/        # Project management module
│   ├── weekly/          # Weekly reports/journals module
│   ├── user/            # User management (custom auth flow)
│   └── house/           # Property/house management module
├── templates/           # HTML templates
├── static/             # Static files (CSS, JS)
├── utils/              # Utility scripts (db_backup, encrypt_tool, etc.)
├── media/              # User-uploaded content
├── dbback/             # Database backups
└── logs/               # Application logs
```

### Django Apps Overview

**apps/core/** - Contains base models with common fields (timestamps, etc.) used across other apps

**apps/projects/** - Project management with:
- Eisenhower Matrix priority system
- Rich text execution steps (multiple editor support)
- File attachments
- Public/private visibility
- Progress tracking with duration calculation

**apps/weekly/** - Weekly journal/reports with:
- Life expectancy tracking and remaining time calculations
- Rich content and file attachments
- Public/private visibility

**apps/user/** - Custom user management:
- Supports multiple users per email (non-standard Django behavior)
- Password reset functionality
- Custom middleware for admin access
- One-to-one user profile extension (`UserForWeekly` model)

**apps/house/** - Property management:
- House listings with details
- Rental status tracking
- Monthly expense/income tracking
- Item inventory management

### Key Architecture Patterns

**Permission Model**: All users can access the Django admin interface, but permissions are restricted:
- Regular users: Full permissions on their own content, read-only on public content
- Superusers: Full access to everything

**Rich Text Editors**: The system supports multiple editors (CKEditor, TinyMCE, MarkdownX, MDEditor, Vditor). Most models use CKEditor as the default.

**Admin-Centric Design**: The entire application is built around Django's admin interface rather than custom views.

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:
- `EMAIL_HOST_USER` - SMTP email for password reset
- `EMAIL_HOST_PASSWORD` - SMTP password

### Settings File

- Main settings: `project_sys/settings.py`
- Local overrides: `project_sys/local_settings.py` (imported at end of settings.py)
- Debug mode is enabled by default in development
- Language: `zh-hans` (Chinese), Timezone: `Asia/Shanghai`

### Static Files

- Development: Served via Django
- Production: Served via Whitenoise middleware
- Static root: `collected_static/`
- Media root: `media/`

## Important Notes

### User System Quirk

This project intentionally allows multiple users to register with the same email address. This is non-standard behavior for Django and was implemented as a feature.

### Database

- Development uses SQLite (`db.sqlite3`)
- For production, consider PostgreSQL or MySQL

### Backup System

Utilities in `utils/` provide:
- Database backup (`db_backup.py`)
- File encryption (`encrypt_tool.py`)
- Path management (`path_manager.py`)

These are manually run scripts - there's a TODO to convert them to Celery tasks.

### Logging

Logs are stored in `logs/` directory:
- `all.log` - Rotating file handler (5MB max, 3 backups)
- `all_time.log` - Time-based rotation (daily)
- Console logging when DEBUG=True
