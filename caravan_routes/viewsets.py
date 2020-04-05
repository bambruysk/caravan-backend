from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from caravan_routes.models import GeoPoint, RoutePoint, Route, GeoMap
from caravan_routes.serializers import GeoPointSerializer, RoutePointSerializer, RouteSerializer, GeoMapSerializer


class GeoPointViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = GeoPoint.objects.all()
    serializer_class = GeoPointSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class RoutePointViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = RoutePoint.objects.all()
    serializer_class = RoutePointSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class RouteViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class GeoMapViewSet(viewsets.ModelViewSet):
    queryset = GeoMap.objects.all()
    serializer_class = GeoMapSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CurrentStatViewSet(viewsets.GenericViewSet):
    serializer_class = GeoMapSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, pk=None):
        user: User = request.user
        caravan = user.caravan

    #    caravan.state =
