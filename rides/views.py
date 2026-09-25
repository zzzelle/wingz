from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from lib.filters import DistanceOrderingFilter, RideFilter
from rides.models import Ride, RideEvent
from rides.serializers import RideSerializer, RideEventSerializer


@extend_schema(tags=["Ride"])
@extend_schema_view(
    list=extend_schema(
        operation_id="List rides",
        description="Returns a list of all `rides`.",
    ),
    create=extend_schema(
        operation_id="Create a ride",
        description="Creates a new `ride`.",
    ),
    retrieve=extend_schema(
        operation_id="Retrieve a ride",
        description="Retrieves the details of an existing `ride`.",
    ),
    update=extend_schema(
        operation_id="Fully update a ride",
        description="Fully updates an existing `ride`.<br>"
        "*All the previous values of the `ride` will be replaced with the new values provided. "
        "Any parameters not provided will be unset.*",
    ),
    partial_update=extend_schema(
        operation_id="Update a ride",
        description="Updates an existing `ride`.<br>"
        "*Only the parameters specified will be updated while the rest will be left unchanged.*",
    ),
    destroy=extend_schema(
        operation_id="Delete a ride",
        description="Deletes an existing `ride`.",
    ),
)
class RideViewSet(viewsets.ModelViewSet):
    queryset = (
        Ride.objects.all()
        .select_related("id_rider", "id_driver")
        .prefetch_related("ride_events")
        .order_by("-id_ride")
    )
    serializer_class = RideSerializer
    filter_backends = [DjangoFilterBackend, DistanceOrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ["pickup_time", "distance"]


@extend_schema(tags=["RideEvent"])
@extend_schema_view(
    list=extend_schema(
        operation_id="List ride events",
        description="Returns a list of all `ride events`.",
    ),
    create=extend_schema(
        operation_id="Create a ride event",
        description="Creates a new `ride event`.",
    ),
    retrieve=extend_schema(
        operation_id="Retrieve a ride event",
        description="Retrieves the details of an existing `ride event`.",
    ),
    update=extend_schema(
        operation_id="Fully update a ride event",
        description="Fully updates an existing `ride event`.<br>"
        "*All the previous values of the `ride event` will be replaced with the new values provided. "
        "Any parameters not provided will be unset.*",
    ),
    partial_update=extend_schema(
        operation_id="Update a ride event",
        description="Updates an existing `ride event`.<br>"
        "*Only the parameters specified will be updated while the rest will be left unchanged.*",
    ),
    destroy=extend_schema(
        operation_id="Delete a ride event",
        description="Deletes an existing `ride event`.",
    ),
)
class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
