from django.apps import AppConfig


class CaravanRoutesConfig(AppConfig):
    name = 'caravan_routes'


from scripts.geopoint_loader import load_geopoint, make_default_points, \
    make_route_from_json  # , delete_routes
