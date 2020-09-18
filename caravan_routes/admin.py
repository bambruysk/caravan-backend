from django.contrib import admin

# Register your models here.
from caravan_routes.models import GeoPoint, RoutePoint, Route, GeoMap, Caravan, Artifact, Pincode

admin.site.register(GeoPoint)
admin.site.register(RoutePoint)
admin.site.register(Route)
admin.site.register(GeoMap)
admin.site.register(Caravan)
admin.site.register(Artifact)
admin.site.register(Pincode)