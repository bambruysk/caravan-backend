from django.db import models
from math import sqrt
from django.utils import timezone

# Create your models here.


# Geopoints


class GeoPoint (models.Model):
    lattitude = models.DecimalField(max_digits=10,decimal_places=7)
    longitude = models.DecimalField(max_digits=10,decimal_places=7)
    name = models.CharField(max_length=32)

    def __str__ (self):
        return self.name

    def isNear(self, latt, long, max_dist = 20):
        """

        :type max_dist: float
        """
        len = sqrt((latt-self.lattitude)**2 + (long-self.longitude)**2)
        return len < max_dist

class RoutePoint(models.Model):
    name = models.CharField(max_length=32)
    position = models.ForeignKey(GeoPoint,on_delete=models.CASCADE) # need be fixed on_delete
    description =  models.CharField(max_length=20000)

    def __str__ (self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=20000)
    points = models.ManyToManyField(RoutePoint)
    last_update = models.DateTimeField(default=timezone.now)


class Caravan(models.Model):
    name = models.CharField(max_length=32)
    state = models.CharField(max_length=8)
    lattitude = models.DecimalField(max_digits=10,decimal_places=7)
    longitude = models.DecimalField(max_digits=10,decimal_places=7)
    quest = models.ForeignKey(Route,on_delete=models.PROTECT)
    quest_progress = models.ForeignKey(RoutePoint,on_delete=models.PROTECT)
    last_connect_time = models.DateTimeField(default=timezone.now)


class RouteCollection(models.Model):
    version = models.BigIntegerField()
    routes = models.ManyToManyField(Route)