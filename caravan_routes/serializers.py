from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Route, GeoPoint, RoutePoint, GeoMap, Caravan, Artifact, GameModel, PlayHistory


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
        fields = '__all__'


class GeoPointIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoPoint
        fields = ['id', ]

class GeoPointCoordOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoPoint
        fields = ['latitude', "longitude"]


class RoutePointSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    # position = GeoPointSerializer(many=False, read_only=True)
    point_id = serializers.IntegerField(source="id")

    class Meta:
        model = RoutePoint
        fields = ['route_id', 'description', 'position', 'name', 'point_id', "point_type"]


class RoutePointShortSerializer(serializers.ModelSerializer):
    # position = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    # position = GeoPointSerializer(many=False, read_only=True)
    seq_id = serializers.IntegerField(source="id")
    geo_id = serializers.PrimaryKeyRelatedField(source="position", read_only=True)

    class Meta:
        model = RoutePoint
        fields = ['seq_id', 'geo_id', 'message', "point_type"]



#
# class RouteSerializer(serializers.ModelSerializer):
#     points = RoutePointSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Route
#         fields = ['id', 'description', 'name', 'points', 'last_update']


class RouteSerializer(serializers.ModelSerializer):
    #    route_id = serializers.IntegerField(source="route_id")
    route_name = serializers.CharField(source="name")
    route_level = serializers.IntegerField(source="level")
    route_description = serializers.CharField(source='description')
    master_instruction = serializers.CharField(source="instruction")
    points = RoutePointShortSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['route_id',
                  'route_name',
                  'route_level',
                  'route_description',
                  "master_instruction",
                  'points',
                  "map_visible",
                  "route_visible",
                  "ordered",
                  'last_update'
                  ]


class RouteShortSerializer(serializers.ModelSerializer):
    # route_id = serializers.IntegerField(source="id")
    route_name = serializers.CharField(source="name")
    route_level = serializers.IntegerField(source="level")
    route_description = serializers.CharField(source='description')
    master_instruction = serializers.CharField(source="instruction")

    class Meta:
        model = Route
        fields = ['route_id',
                  'route_name',
                  'route_level',
                  'route_description',
                  "master_instruction",
                  "map_visible",
                  "route_visible",
                  "ordered",
                  'last_update'
                  ]


"""
    map_visible = serializers.BooleanField(source="map_visible")
    route_visible = serializers.BooleanField(source="route_visible")
    ordered = serializers.BooleanField(source="ordered") # прохождение по порядку
"""


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


class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artifact
        fields = '__all__'


class GameModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameModel


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayHistory
