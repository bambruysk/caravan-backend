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
        fields = ['id', 'name', 'lattitude', "longitude"]


class RoutePointSerializer(serializers.ModelSerializer):
    geopoints = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = RoutePoint
        fields = ['id', 'description', 'name', 'geopoints']


class RouteSerializer(serializers.ModelSerializer):
    points = RoutePointSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'description', 'name', 'points', 'last_update']
