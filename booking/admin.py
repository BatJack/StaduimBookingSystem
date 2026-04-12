from django.contrib import admin
from .models import Court, CourtAvailability, Booking


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(CourtAvailability)
class CourtAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['court', 'date', 'start_time', 'end_time', 'created_at', 'updated_at']
    list_filter = ['court', 'date']
    date_hierarchy = 'date'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'court', 'date', 'start_time', 'end_time', 'status', 'created_at']
    list_filter = ['court', 'date', 'status']
    search_fields = ['user__username', 'court__name']
    date_hierarchy = 'date'
