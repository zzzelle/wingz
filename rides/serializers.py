from datetime import timedelta
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from rides.models import Ride, RideEvent
from users.serializers import UserSerializer


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ["id_ride_event", "id_ride", "description", "created_at"]
        read_only_fields = ["id_ride_event", "created_at"]


class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer(source="id_rider", read_only=True)
    driver = UserSerializer(source="id_driver", read_only=True)
    ride_events = RideEventSerializer(many=True, read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    @extend_schema_field(RideEventSerializer(many=True))
    def get_todays_ride_events(self, obj):
        # Even though the field name is today, we're actually getting the last 24 hours
        # as specified in the requirements.
        last_24h = timezone.now() - timedelta(hours=24)
        todays_events = [e for e in obj.ride_events.all() if e.created_at >= last_24h]
        return RideEventSerializer(todays_events, many=True).data

    class Meta:
        model = Ride
        fields = [
            "id_ride",
            "status",
            "id_rider",
            "id_driver",
            "rider",
            "driver",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
            "ride_events",
            "todays_ride_events",
        ]
        read_only_fields = ["id_ride"]
        extra_kwargs = {
            "id_rider": {"write_only": True},
            "id_driver": {"write_only": True},
        }
