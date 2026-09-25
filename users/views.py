from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.models import User
from users.serializers import UserSerializer


@extend_schema(tags=["User"])
@extend_schema_view(
    list=extend_schema(
        operation_id="List users",
        description="Returns a list of all `users`.",
    ),
    create=extend_schema(
        operation_id="Create a user",
        description="Creates a new `user`.",
    ),
    retrieve=extend_schema(
        operation_id="Retrieve a user",
        description="Retrieves the details of an existing `user`.",
    ),
    update=extend_schema(
        operation_id="Fully update a user",
        description="Fully updates an existing `user`.<br>"
        "*All the previous values of the `user` will be replaced with the new values provided. "
        "Any parameters not provided will be unset.*",
    ),
    partial_update=extend_schema(
        operation_id="Update a user",
        description="Updates an existing `user`.<br>"
        "*Only the parameters specified will be updated while the rest will be left unchanged.*",
    ),
    destroy=extend_schema(
        operation_id="Delete a user",
        description="Deletes an existing `user`.",
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=["Token"])
@extend_schema_view(
    post=extend_schema(
        operation_id="Obtain token",
        description="Obtains the `access token`. "
        f"Expiration lasts for {settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']}.",
    ),
)
class TokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=["Token"])
@extend_schema_view(
    post=extend_schema(
        operation_id="Refresh token",
        description="Refreshes the `access token`. "
        f"Expiration is also reset back to {settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']}.",
    ),
)
class TokenRefreshView(TokenRefreshView):
    pass
