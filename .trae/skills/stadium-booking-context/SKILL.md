---
name: "stadium-booking-context"
description: "Provides project structure and UI editing guidelines for Stadium Booking System. Invoke BEFORE modifying any code to understand project architecture."
---

# Stadium Booking System Context

This skill provides essential context about the Stadium Booking System project structure and editing guidelines.

## When to Invoke

**ALWAYS invoke this skill BEFORE:**
- Modifying any UI templates
- Adding new features
- Refactoring code
- Making structural changes to the project

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
   └── admin_*.html         # Admin pages
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

## Reference Document

For complete project documentation, read:
`.trae/docs/stadium-booking-project.md`

## Quick Checklist Before Editing

- [ ] Read the project documentation
- [ ] Identify the correct file to modify
- [ ] Follow existing naming conventions
- [ ] Maintain template inheritance structure
- [ ] Run migrations if models change
