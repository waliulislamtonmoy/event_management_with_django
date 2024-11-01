from django.contrib import admin
from event.models import Event, Booking


class EventAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('name', 'location', 'date')
    search_fields = ('name', 'location')  # Searchable fields
    list_filter = ('date',)  # Filter options in the sidebar


class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', )  # Display booking info
    search_fields = ('user__username', 'event__name')  # Searchable fields


admin.site.register(Event, EventAdmin)
admin.site.register(Booking, BookingAdmin)
