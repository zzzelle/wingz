from django.contrib import admin
from unfold.admin import ModelAdmin

from rides.models import Ride, RideEvent


class RideEventInline(admin.TabularInline):
    model = RideEvent
    extra = 0
    fields = ["description", "created_at"]
    readonly_fields = ["created_at"]


@admin.register(Ride)
class RideAdmin(ModelAdmin):
    list_display = ["id_ride", "status", "id_rider", "id_driver", "pickup_time"]
    list_filter = ["status", "pickup_time"]
    search_fields = ["id_rider__email", "id_driver__email"]
    # Join rider and driver in the list query instead of one query per row.
    list_select_related = ["id_rider", "id_driver"]
    autocomplete_fields = ["id_rider", "id_driver"]
    inlines = [RideEventInline]
