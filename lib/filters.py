import django_filters

from django.db.models import ExpressionWrapper, F, FloatField, Value
from django.db.models.functions import ASin, Cos, Power, Radians, Sin, Sqrt
from rest_framework import filters, serializers

from rides.models import Ride


class RideFilter(django_filters.FilterSet):
    rider__email = django_filters.CharFilter(
        field_name="id_rider__email", lookup_expr="iexact", label="Rider Email"
    )

    class Meta:
        model = Ride
        fields = ["rider__email", "status"]


class DistanceOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if not ordering:
            return queryset

        if any(f.lstrip("-") == "distance" for f in ordering):
            errors = {}
            lat = self.validate_lat_lng(request, "lat", 90, errors)
            lng = self.validate_lat_lng(request, "lng", 180, errors)
            if errors:
                raise serializers.ValidationError(errors)

            queryset = self.annotate_distance(queryset, lat, lng)
            ordering = [f.replace("distance", "distance_km") for f in ordering]

        return queryset.order_by(*ordering)

    def annotate_distance(self, qs, lat, lng):
        """
        Annotate the queryset with a calculated distance in km from the given lat/lng
        to the pickup location. Uses the Haversine formula to calculate the distance.
        """

        # 1. Convert decimal degrees to radians
        lat1 = Radians(Value(lat))
        lng1 = Radians(Value(lng))
        lat2 = Radians(F("pickup_latitude"))
        lng2 = Radians(F("pickup_longitude"))

        # 2. Differences between the two points
        dlat = lat2 - lat1
        dlng = lng2 - lng1

        # 3. Calculate a (the Haversine of the central angle)
        #    a = sin²(dlat/2) + cos(lat1) * cos(lat2) * sin²(dlng/2)
        a = Power(Sin(dlat / 2), 2) + Cos(lat1) * Cos(lat2) * Power(Sin(dlng / 2), 2)

        # 4. Calculate c (the central angle in radians)
        #    c = 2 * asin(√a)
        c = 2 * ASin(Sqrt(a))

        # 5. Calculate the Final Distance (\[d\]):
        #    d = r * c, with r = Earth's radius in km (use 3956 for miles)
        r = 6371.0

        return qs.annotate(
            distance_km=ExpressionWrapper(r * c, output_field=FloatField())
        )

    def validate_lat_lng(self, request, param, limit, errors):
        """
        Validate a lat/lng query parameter.
        Returns the value already typecasted in float if valid,
        otherwise adds an error to the errors dict.
        """
        value = request.query_params.get(param)

        if not value:
            errors[param] = ["This parameter is required when ordering by distance."]
        else:
            try:
                value = float(value)
                if not (-limit <= value <= limit):
                    errors[param] = [f"Must be between -{limit} and {limit}."]
            except ValueError:
                errors[param] = [f"A valid number is required, got '{value}'."]

        return value

    def to_html(self, request, queryset, view):
        # Hide the ordering widget in the browsable API to avoid confusion, since
        # it only allows 1 selection but multiple ordering fields are actually allowed.
        # The user can still use the query parameter directly.
        return ""
