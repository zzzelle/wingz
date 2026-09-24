from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from lib.filters import DistanceOrderingFilter, RideFilter
from rides.models import Ride, RideEvent
from rides.serializers import RideSerializer, RideEventSerializer


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all().prefetch_related('ride_events').order_by('-id_ride')
    serializer_class = RideSerializer
    filter_backends = [DjangoFilterBackend, DistanceOrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time', 'distance']


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    http_method_names=['post', 'delete']
