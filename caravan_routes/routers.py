from rest_framework import routers

from caravan_routes.viewsets import GeoPointViewSet, RoutePointViewSet, RouteViewSet, GeoMapViewSet, QuestBuildViewSet, \
    RouteShortViewSet, ArtifactViewSet, GameViewSet

router = routers.SimpleRouter()
router.register(r'geo_points', GeoPointViewSet)
router.register(r'routepoints', RoutePointViewSet)
router.register(r'routes', RouteShortViewSet)
router.register(r'routes_full', RouteViewSet)
router.register(r'game_map', GeoMapViewSet)
router.register(r'artifacts', ArtifactViewSet)
# router.register(r'play',PlayViewSet)
# router.register(r'quest_build', QuestBuildViewSet)
router.register(r'game', GameViewSet)
