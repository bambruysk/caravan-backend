from django.db import models
from math import sqrt

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Create your models here.


# Geopoints


class GeoPoint(models.Model):
    lattitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name} latt={self.lattitude} long={self.longitude}"

    def isNear(self, latt, long, max_dist=20):
        """

        :type max_dist: float
        """
        len = sqrt((latt - self.lattitude) ** 2 + (long - self.longitude) ** 2)
        return len < max_dist


def make_default_points():
    GeoPoint.objects.get_or_create(name="north_west")
    GeoPoint.objects.get_or_create(name="north_east")
    GeoPoint.objects.get_or_create(name="south_west")
    GeoPoint.objects.get_or_create(name="south_east")


make_default_points()


class RoutePoint(models.Model):
    name = models.CharField(max_length=32)
    position = models.ForeignKey(GeoPoint, on_delete=models.CASCADE,
                                 related_name='position')  # need be fixed on_delete
    description = models.TextField(max_length=20000)

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=20000)
    points = models.ManyToManyField(RoutePoint, related_name='points')
    last_update = models.DateTimeField(default=timezone.now)
    level = models.IntegerField(default=0)
    instruction = models.TextField(max_length=20000, default="")

    def __str__(self):
        return self.name


class Caravan(models.Model):
    name = models.CharField(max_length=32)
    state = models.CharField(max_length=8)
    lattitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    quest = models.ForeignKey(Route, on_delete=models.PROTECT, null=True, blank=True)
    quest_progress = models.ForeignKey(RoutePoint, on_delete=models.PROTECT, null=True, blank=True)
    last_connect_time = models.DateTimeField(default=timezone.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

    def update(self, data: CaravanState):




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Caravan.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.caravan.save()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# class RouteCollection(models.Model):
#     version = models.BigIntegerField()
#     routes = models.ManyToManyField(Route)


class Team(models.Model):
    name = models.CharField(max_length=60)
    routes = models.ManyToManyField(Route)


class GeoMap(models.Model):
    name = models.CharField(max_length=60)
    picture = models.FileField(upload_to='maps/')

    north_west = models.ForeignKey(GeoPoint,
                                   on_delete=models.CASCADE,
                                   related_name="north_west",
                                   default=None)

    north_east = models.ForeignKey(GeoPoint,
                                   on_delete=models.CASCADE,
                                   related_name="north_east",
                                   default=None)

    south_west = models.ForeignKey(GeoPoint,
                                   on_delete=models.CASCADE,
                                   related_name="south_west",
                                   default=None)

    south_east = models.ForeignKey(GeoPoint,
                                   on_delete=models.CASCADE,
                                   related_name="south_east",
                                   default=None)

    description = models.TextField(max_length=2000, default="")


# @receiver(post_save, sender=GeoMap)
def set_default_to_mape(sender, instance=None, created=False, **kwargs):
    """
    Just for debugging. set default postiont to maps
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        if instance:
            instance.south_east = GeoPoint.objects.get_or_create(name="south_east")
            instance.south_west = GeoPoint.objects.get_or_create(name="south_west")
            instance.north_west = GeoPoint.objects.get_or_create(name="north_west")
            instance.north_east = GeoPoint.objects.get_or_create(name="north_east")


#
# for username in Caravan.objects.all():
#     Token.objects.get_or_create(user=username)

def create_superuser_caravan():
    admin = User.objects.get(username='odmen')
    if admin:
        car = Caravan.objects.create(user=admin)
        print("Caravan for odmen created")
    else:
        print("Odmen not found")

# create_superuser_caravan()
