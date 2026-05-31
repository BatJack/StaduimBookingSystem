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

This is a Django-based badminton court booking system with the following features:
- Court booking and management
- Student course booking system
- User authentication and authorization
- Admin dashboard for system management

## Project Structure

### Root Directory Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management script |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |
| `create_user.py` | User creation script (web) |
| `create_user_cli.py` | User creation script (CLI) |
| `update.sh` | Server update script |
| `.gitignore` | Git ignore rules |

### Main Application (`booking/`)

| File/Directory | Purpose |
|----------------|---------|
| `models.py` | Data models (User, Court, Booking, Student, etc.) |
| `views.py` | Business logic and view functions |
| `urls.py` | URL routing configuration |
| `tests.py` | Unit tests |
| `admin.py` | Django admin configuration |
| `apps.py` | Application configuration |
| `migrations/` | Database migration files |
| `templates/booking/` | UI templates |

### Project Configuration (`stadium_booking/`)

| File | Purpose |
|------|---------|
| `settings.py` | Development settings |
| `settings_production.py` | Production settings |
| `urls.py` | Project-level URL routing |
| `wsgi.py` | WSGI deployment config |
| `asgi.py` | ASGI deployment config |

### Documentation & Skills (`.trae/`)

| Directory | Purpose |
|-----------|---------|
| `docs/` | Project documentation |
| `docs/issues/` | Issue tracking and solutions |
| `skills/` | Trae AI skill definitions |

### Assets (`assets/`)

| File | Purpose |
|------|---------|
| `*.png` | UI screenshots |
| `configuration_server.md` | Server configuration guide |

## URL Routing Rules

**CRITICAL: URL Conflict Resolution**

The project has TWO admin systems that must NOT conflict:

| System | Path Prefix | Description |
|--------|-------------|-------------|
| Django Admin | `/admin/` | Django's built-in admin (for database management) |
| Custom Admin | `/manage/` | Custom management pages (main admin interface) |

### URL Patterns

**Public URLs:**
- `/` - Login page
- `/logout/` - Logout
- `/courts/` - Court listing and booking
- `/my-bookings/` - User's bookings
- `/cancel-booking/<id>/` - Cancel a booking

**API Endpoints:**
- `/api/time-slots/` - Get available time slots
- `/api/create-booking/` - Create a new booking

**Admin URLs (all under `/manage/`):**
- `/manage/` - Admin dashboard
- `/manage/statistics/` - Statistics and reports
- `/manage/courts/` - Court management
- `/manage/court-types/` - Court type management
- `/manage/availabilities/` - Court availability management
- `/manage/bookings/` - Booking management
- `/manage/students/` - Student management
- `/manage/course-bookings/` - Course booking management

**IMPORTANT RULES:**
1. NEVER use `admin/` as a path prefix in `booking/urls.py` - it will conflict with Django Admin
2. ALWAYS use `manage/` as the path prefix for custom admin pages
3. When adding new admin features, use paths like `manage/feature-name/`
4. The `name` parameter in URL patterns can still contain "admin" (e.g., `name='admin_dashboard'`) - only the path prefix matters

## UI Templates Structure

### Base Template
- **File**: `booking/templates/booking/base.html`
- Contains all global CSS styles
- All other templates inherit from this
- Includes navigation bar and common layout

### Template Hierarchy

```
base.html (base template with global styles and navigation)
│
├── Public Pages
│   ├── login.html              # Login page
│   ├── court_list.html         # Court listing and booking
│   ├── booking_form.html       # Booking form
│   └── my_bookings.html        # User's bookings
│
├── Admin Pages (all under /manage/ paths)
│   ├── admin_dashboard.html    # Admin dashboard (main entry)
│   ├── admin_statistics.html   # Statistics and reports
│   │
│   ├── admin_court_list.html   # Court management
│   ├── admin_court_form.html   # Add/edit court
│   │
│   ├── admin_court_type_list.html    # Court type management
│   ├── admin_court_type_form.html    # Add/edit court type
│   │
│   ├── admin_availability_list.html  # Availability management
│   ├── admin_availability_form.html  # Add availability
│   │
│   ├── admin_bookings.html          # Booking management
│   ├── admin_booking_form.html      # Add booking
│   ├── admin_booking_edit.html      # Edit booking
│   │
│   ├── admin_student_list.html      # Student management
│   ├── admin_student_form.html      # Add/edit student
│   │
│   ├── admin_course_booking_list.html   # Course booking management
│   ├── admin_course_booking_form.html   # Add course booking
│   └── admin_course_booking_edit.html   # Edit course booking
│
└── Includes (reusable components)
    ├── page_header.html    # Page header component
    ├── stat_card.html      # Statistics card component
    ├── data_table.html     # Data table component
    └── empty_state.html    # Empty state component
```

### Editing Rules

1. **Global styles** → Edit `base.html` `<style>` section
2. **Page layout** → Edit specific template file
3. **Navigation** → Edit `base.html` `.nav` section
4. **New page** → Create template extending `base.html`
5. **Reusable components** → Create in `templates/booking/includes/`

## Data Models

### Core Models

| Model | Description | Key Fields |
|-------|-------------|------------|
| `User` | Django built-in user model | username, password, email |
| `Profile` | User profile with type | user, user_type (admin/regular) |
| `CourtType` | Court type classification | name (unique), is_default |
| `Court` | Court information | court_type, name, court_number, description |
| `CourtAvailability` | Court availability schedule | court, start_date, end_date, start_time, end_time |
| `Booking` | Booking record | booking_type, user, court, date, start_time, end_time, status |
| `Student` | Student information | name, phone, total_class_hours |
| `BookingStudent` | Booking-student relationship | booking, student, class_hours |

### Model Relationships

```
User (1:1) Profile
User (1:N) Booking
CourtType (1:N) Court
Court (1:N) CourtAvailability
Court (1:N) Booking
Booking (1:N) BookingStudent (N:1) Student
```

## Backend Editing Guide

### Adding New Features

1. **Define data model** → `models.py`
   - Create model class
   - Define fields and relationships
   - Add `__str__` method
   - Set `Meta` options

2. **Create migration** → Run `python manage.py makemigrations`
3. **Apply migration** → Run `python manage.py migrate`

4. **Implement business logic** → `views.py`
   - Create view function
   - Add permission checks
   - Handle form data
   - Return response

5. **Add URL route** → `urls.py`
   - Use appropriate path prefix (`/manage/` for admin)
   - Set meaningful name

6. **Create template** → `templates/booking/`
   - Extend `base.html`
   - Implement UI
   - Add to navigation if needed

### Business Logic Patterns

- **Permission check**: Use `is_admin_user(request.user)` for admin-only views
- **Login required**: Use `@login_required` decorator
- **Messages**: Use Django messages framework for user feedback
- **Error handling**: Use try-except and return appropriate error responses

## Session Configuration

Sessions use cache-backed storage (LocMemCache):
- Sessions are lost on server restart
- Users must re-login after server restart
- Configured in `stadium_booking/settings.py`
- Session engine: `django.contrib.sessions.backends.cache`

## Testing

### Test Structure

- **File**: `booking/tests.py`
- **Test Classes**:
  - `ModelTests` - Data model tests
  - `AuthenticationTests` - Authentication tests
  - `CourtListTests` - Court listing and booking tests
  - `AdminTests` - Admin functionality tests
  - `PermissionTests` - Permission and access control tests

### Running Tests

```bash
# Run all tests
python manage.py test booking.tests

# Run specific test class
python manage.py test booking.tests.ModelTests

# Run with verbose output
python manage.py test booking.tests --verbosity=2
```

### Test Data Patterns

- Use `get_or_create` for shared data (e.g., CourtType)
- Create test users with different types (admin/regular)
- Clean up data in `tearDown` if needed

## Quick Checklist Before Editing

- [ ] Read the project documentation
- [ ] Identify the correct file to modify
- [ ] Follow existing naming conventions
- [ ] Maintain template inheritance structure
- [ ] Run migrations if models change
- [ ] **NEVER use `admin/` path prefix in booking/urls.py**
- [ ] **ALWAYS use `manage/` path prefix for custom admin pages**
- [ ] Test changes with appropriate user types
- [ ] Update tests if adding new features

## Common Tasks

### Adding a New Admin Page

1. Create view function in `views.py`:
```python
@login_required
def admin_new_feature(request):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    # ... implementation
    return render(request, 'booking/admin_new_feature.html', context)
```

2. Add URL in `urls.py`:
```python
path('manage/new-feature/', views.admin_new_feature, name='admin_new_feature'),
```

3. Create template extending `base.html`

4. Add navigation link in `base.html` if needed

### Adding a New API Endpoint

1. Create view function in `views.py`:
```python
@login_required
def api_new_endpoint(request):
    # ... implementation
    return JsonResponse({'success': True, 'data': data})
```

2. Add URL in `urls.py`:
```python
path('api/new-endpoint/', views.api_new_endpoint, name='api_new_endpoint'),
```

3. Test with different HTTP methods (GET, POST)

### Modifying Database Schema

1. Edit `models.py`
2. Create migration: `python manage.py makemigrations`
3. Review migration file
4. Apply migration: `python manage.py migrate`
5. Update tests if needed
6. Update documentation
