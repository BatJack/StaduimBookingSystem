---
name: "stadium-booking-context"
description: "Provides project structure, URL routing rules, and UI editing guidelines for Stadium Booking System. Invoke BEFORE modifying any code to understand project architecture and avoid URL conflicts."
---

# Stadium Booking System Context

This skill provides essential context about the Stadium Booking System project structure and editing guidelines.

## When to Invoke

**ALWAYS invoke this skill BEFORE:**
- Modifying any UI templates
- Adding new features
- Refactoring code
- Making structural changes to the project
- Changing URL routing

## Project Overview

This is a Django-based badminton court booking system.

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `booking/templates/booking/` | All UI templates |
| `booking/views.py` | Business logic |
| `booking/models.py` | Data models |
| `booking/urls.py` | URL routing |
| `stadium_booking/` | Project settings |

## URL Routing Rules

**CRITICAL: URL Conflict Resolution**

The project has TWO admin systems that must NOT conflict:

| System | Path Prefix | Description |
|--------|-------------|-------------|
| Django Admin | `/admin/` | Django's built-in admin (for database management) |
| Custom Admin | `/manage/` | Custom management pages (main admin interface) |

**IMPORTANT RULES:**
1. NEVER use `admin/` as a path prefix in `booking/urls.py` - it will conflict with Django Admin
2. ALWAYS use `manage/` as the path prefix for custom admin pages
3. When adding new admin features, use paths like `manage/feature-name/`
4. The `name` parameter in URL patterns can still contain "admin" (e.g., `name='admin_dashboard'`) - only the path prefix matters

## UI Editing Guide

### Base Template
- **File**: `booking/templates/booking/base.html`
- Contains all global CSS styles
- All other templates inherit from this

### Template Structure
```
base.html
   ├── court_list.html      # Court listing
   ├── booking_form.html    # Booking form
   ├── my_bookings.html     # User bookings
   ├── login.html           # Login page
   └── admin_*.html         # Admin pages (under /manage/ paths)
```

### Editing Rules

1. **Global styles** → Edit `base.html` `<style>` section
2. **Page layout** → Edit specific template file
3. **Navigation** → Edit `base.html` `.nav` section
4. **New page** → Create template extending `base.html`

## Backend Editing Guide

1. **New feature** → models.py → views.py → urls.py
2. **Business logic** → views.py
3. **Database changes** → Run migrations
4. **New admin page** → Use `manage/` path prefix, NOT `admin/`

## Session Configuration

Sessions use cache-backed storage (LocMemCache):
- Sessions are lost on server restart
- Users must re-login after server restart
- Configured in `stadium_booking/settings.py`

## Quick Checklist Before Editing

- [ ] Read the project documentation
- [ ] Identify the correct file to modify
- [ ] Follow existing naming conventions
- [ ] Maintain template inheritance structure
- [ ] Run migrations if models change
- [ ] **NEVER use `admin/` path prefix in booking/urls.py**
- [ ] **ALWAYS use `manage/` path prefix for custom admin pages**
