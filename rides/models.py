from django.db import models

from users.models import User


class Ride(models.Model):
    STATUS_ENROUTE = "en-route"
    STATUS_PICKUP = "pickup"
    STATUS_DROPOFF = "dropoff"
    STATUS_CHOICES = [
        (STATUS_ENROUTE, "En Route"),
        (STATUS_PICKUP, "Pickup"),
        (STATUS_DROPOFF, "Dropoff"),
    ]

    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PICKUP)
    id_rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rider_rides')
    id_driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_rides')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"[Ride {self.id_ride} - {self.status}]  Driver: {self.id_driver.email}, Rider: {self.id_rider.email}"

    class Meta:
        ordering = ["-id_ride"]


class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='ride_events')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["created_at"]
