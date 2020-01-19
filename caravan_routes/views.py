from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from caravan_routes.models import GeoPoint, RouteCollection, Route
from django.forms import ModelForm
from django_tables2.tables import Table
from django_tables2.views import SingleTableView
from django.http import HttpRequest, HttpResponse, JsonResponse

# Create your views here.


class GeoPointsView(ListView):
    model = GeoPoint


class GeoPointTable(Table):
    class Meta:
        model = GeoPoint

class GeoPointTableView(SingleTableView):
    table_class = GeoPointTable
    queryset = GeoPoint.objects.all()
    template_name = "caravan_routes/geopoint_table.html"

class GeoPointsCreateView(CreateView):
    model = GeoPoint
    fields = ['name',
              'lattitude',
              'longitude']


class GeoPointsModelForm(ModelForm):
    class Meta:
        model = GeoPoint
        fields = ['name',
                  'lattitude',
                  'longitude']



def check_version(req  ):
    version = req.GET.get("version",0)
    #
    last_route_coll = RouteCollection.objects.all().order_by(version)[:1]
    if last_route_coll.version > version:
        return HttpResponse("UPDATE")
    else:
        return HttpResponse("OK")

def update (req):
    routes = Route.objects.all()
    return JsonResponse(routes)

