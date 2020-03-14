from rest_framework import routers

from caravan_routes.viewsets import GeoPointViewSet, RoutePointViewSet, RouteViewSet, GeoMapViewSet

router = routers.SimpleRouter()
router.register(r'geopoints', GeoPointViewSet)
router.register(r'routepoints', RoutePointViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'maps', GeoMapViewSet)
