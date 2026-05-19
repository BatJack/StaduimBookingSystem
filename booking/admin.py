from django.contrib import admin
from .models import Court, CourtAvailability, Booking, Student, BookingStudent, CourtType, Profile


@admin.register(CourtType)
class CourtTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_default', 'created_at', 'updated_at']
    list_filter = ['is_default']
    search_fields = ['name']


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['name', 'court_type', 'court_number', 'description', 'created_at', 'updated_at']
    search_fields = ['name', 'court_number']
    list_filter = ['court_type', 'created_at']
    readonly_fields = ['name', 'court_type', 'court_number', 'description', 'created_at', 'updated_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CourtAvailability)
class CourtAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['court', 'start_date', 'end_date', 'start_time', 'end_time', 'created_at', 'updated_at']
    list_filter = ['court', 'start_date']
    date_hierarchy = 'start_date'
    readonly_fields = ['court', 'start_date', 'end_date', 'start_time', 'end_time', 'created_at', 'updated_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_type', 'user', 'court', 'date', 'start_time', 'end_time', 'booker_name', 'status', 'created_at']
    list_filter = ['booking_type', 'court', 'date', 'status']
    search_fields = ['user__username', 'court__name', 'booker_name']
    date_hierarchy = 'date'
    readonly_fields = ['booking_type', 'user', 'court', 'date', 'start_time', 'end_time', 'booker_name', 'booker_phone', 'status', 'created_at', 'updated_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'total_class_hours', 'created_at', 'updated_at']
    search_fields = ['name', 'phone']
    list_filter = ['created_at']
    readonly_fields = ['name', 'phone', 'total_class_hours', 'created_at', 'updated_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BookingStudent)
class BookingStudentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'student', 'class_hours', 'created_at']
    list_filter = ['booking']
    readonly_fields = ['booking', 'student', 'class_hours', 'created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'created_at', 'updated_at']
    list_filter = ['user_type']
    search_fields = ['user__username']
