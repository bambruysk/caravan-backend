from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Route, GeoPoint, RoutePoint


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class GetAllRoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']


class GeoPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoPoint
        fields = ['name','lattitude',"longitude"]


class RoutePointSerializer(serializers.ModelSerializer):
    geopoints = GeoPointSerializer()

    class Meta:
        model = RoutePoint
        fields = ['name', 'description', 'geopoints']
