from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Route, GeoPoint, RoutePoint, GeoMap, Caravan


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


class GeoPointCoordOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoPoint
        fields = ['lattitude', "longitude"]


class RoutePointSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    # position = GeoPointSerializer(many=False, read_only=True)

    class Meta:
        model = RoutePoint
        fields = ['id', 'description', 'name', 'position']


#
# class RouteSerializer(serializers.ModelSerializer):
#     points = RoutePointSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Route
#         fields = ['id', 'description', 'name', 'points', 'last_update']


class RouteSerializer(serializers.ModelSerializer):
    route_id = serializers.IntegerField(source="id")
    route_name = serializers.CharField(source="name")
    route_level = serializers.IntegerField(source="level")
    route_description = serializers.CharField(source='description')
    master_instruction = serializers.CharField(source="instruction")
    points = RoutePointSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['route_id', 'route_name', 'route_level', 'route_description', "master_instruction", 'points',
                  'last_update']


class GeoMapSerializer(serializers.HyperlinkedModelSerializer):
    north_west = GeoPointCoordOnlySerializer(many=False, read_only=True)
    north_east = GeoPointCoordOnlySerializer(many=False, read_only=True)
    south_west = GeoPointCoordOnlySerializer(many=False, read_only=True)
    south_east = GeoPointCoordOnlySerializer(many=False, read_only=True)

    class Meta:
        model = GeoMap
        fields = ['id', 'name', 'description', 'url', 'picture',
                  'north_west', 'north_east', 'south_west', 'south_east']


class CurrentStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caravan
