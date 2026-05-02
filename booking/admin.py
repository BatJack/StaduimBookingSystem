from django.contrib import admin
from .models import Court, CourtAvailability, Booking, Student, BookingStudent


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['created_at']
    readonly_fields = ['name', 'description', 'created_at', 'updated_at']

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
