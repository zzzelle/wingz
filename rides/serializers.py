from rest_framework import serializers

from rides.models import Ride, RideEvent


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = [
            "id_ride_event",
            "id_ride",
            "description",
            "created_at"
        ]
        read_only_fields = ["id_ride_event", "created_at"]
        

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = [
            "id_ride", 
            "status", 
            "id_rider", 
            "id_driver", 
            "pickup_latitude", 
            "pickup_longitude", 
            "dropoff_latitude", 
            "dropoff_longitude", 
            "pickup_time",
        ]
        read_only_fields = ["id_ride"]

