import json

from caravan_routes.models import GeoPoint, RoutePoint, Route


def load_geopoint():
    with open('static/geopoints.json', "r", encoding='utf8') as js_file:
        data = json.load(js_file)
        geopoints_list = data["geo_points"]
        for geopoint in geopoints_list:
            GeoPoint.objects.get_or_create(
                id=int(geopoint["point_id"]),
                name=str(geopoint["label"]),
                latitude=float(geopoint["latitude"]),
                longitude=float(geopoint["latitude"])
            )
            print(geopoint)


def make_default_points():
    borders = {
        "min_latitude": 54.472178,
        "max_latitude": 54.488892,
        "min_longitude": 39.685648,
        "max_longitude": 39.703389
    }
    GeoPoint.objects.get_or_create(name="north_west",
                                   lattitude=borders["max_latitude"],
                                   longitude=borders["min_longitude"])
    GeoPoint.objects.get_or_create(name="north_east",
                                   lattitude=borders["max_latitude"],
                                   longitude=borders["max_longitude"])
    GeoPoint.objects.get_or_create(name="south_west",
                                   lattitude=borders["min_latitude"],
                                   longitude=borders["min_longitude"])
    GeoPoint.objects.get_or_create(name="south_east",
                                   lattitude=borders["min_latitude"],
                                   longitude=borders["max_longitude"])


def delete_routes():
    routes = RoutePoint.objects.all()
    routes.delete()


def make_route_from_json():
    print("Load Route")
    with open('static/route_points.json', "r", encoding='utf8') as js_file:
        import json
        data = json.load(js_file)
        route = data["quest_build"]
        points = route["route_points"]

        rps = []
        for point in points:
            gp = GeoPoint.objects.get(id=int(point["point_id"]))
            rp = RoutePoint.objects.get_or_create(
                name=int(point["route_id"]),
                position=gp,
                route_id=int(point["route_id"]),
                point_type=str(point["point_type"]),
                message=str(point["message"]),
            )
            rps.append(rp)

        Route.objects.get_or_create(
            id=int(route["route_id"]),
            name=str(route["route_name"]),
            level=str(route["route_level"]),
            description=str(route["route_description"]),
            instruction=str(route["master_instruction"]),
            map_visible=bool(route["map_visible"]),
            route_visible=bool(route["route_visible"]),
            ordered=bool(route["ordered"]),

        )


def run():
    load_geopoint()

    make_default_points()
    # delete_routes()
    make_route_from_json()
