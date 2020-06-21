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
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"id={self.id} {self.name} latt={self.latitude} long={self.longitude}"

    def isNear(self, latt, long, max_dist=20):
        """

        :type max_dist: float
        """
        len = sqrt((latt - self.latitude) ** 2 + (long - self.longitude) ** 2)
        return len < max_dist


class RoutePoint(models.Model):
    name = models.CharField(max_length=32, default=" ")
    position = models.ForeignKey(GeoPoint, on_delete=models.CASCADE,
                                 related_name='position')  # need be fixed on_delete
    description = models.TextField(max_length=20000, default="No descr")
    # route order
    route_id = models.IntegerField(default=0)

    message = models.TextField(max_length=20000, default="")

    POINT_CHOSES = [
        ("NECESSARY", "Обязательная"),
        ("OPTIONAL", "Необязательная"),
        ("HIDDEN", "Скрытая"),
    ]
    point_type = models.CharField(max_length=10, choices=POINT_CHOSES, default="NECESSARY")

    def __str__(self):
        return f"{self.id} {self.name}"


class Route(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=20000)
    points = models.ManyToManyField(RoutePoint, related_name='points')
    last_update = models.DateTimeField(default=timezone.now)
    level = models.IntegerField(default=0)
    instruction = models.TextField(max_length=20000, default="")
    route_id = models.IntegerField(default=1)
    # Route options
    map_visible = models.BooleanField(default=True)
    route_visible = models.BooleanField(default=True)  # отображать
    ordered = models.BooleanField(default=True)  # прохождение по порядку

    def __str__(self):
        return str(self.id) + self.name


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

    def __str__(self):
        return str(self.name)


class GameModel(models.Model):
    """
    Current Game settings and info
    """
    map = models.ForeignKey(GeoMap, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=80)
    gamer_name = models.CharField(max_length=80, default="Unknown player")
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING, null=True)


class Caravan(models.Model):
    name = models.CharField(max_length=32)
    state = models.CharField(max_length=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    quest = models.ForeignKey(Route, on_delete=models.PROTECT, null=True, blank=True)
    quest_progress = models.ForeignKey(RoutePoint, on_delete=models.PROTECT, null=True, blank=True)
    last_connect_time = models.DateTimeField(default=timezone.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

    # def update(self, data: CaravanState):


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
'''
artifacts[ // артефакты - Добавление
mac, // mac - адрес - формат'22:e5:63:44:88'
name, // названиеартефакта
description, // описание
auto_init, // флаг автоматической инициализации при нахождении(резервируем на след.версию ПО)
time // время действия артефакта - формат 'час:мин:сек'(резервируем на след.версию ПО)
]
'''


class Artifact(models.Model):
    mac = models.CharField(max_length=20)
    name = models.CharField(max_length=80)
    description = models.TextField()
    auto_init = models.BooleanField()
    time = models.DurationField()

    def __str__(self):
        return str(self.name) + str(self.mac)


"""
        latitude // Широта


longitude // Долгота
last_points // id - пройденных
точек.

< -        last_id // Идентификатор
последнего."""


class PlayHistory(models.Model):
    user_id = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    last_points = models.ManyToManyField(RoutePoint)


class Message(models.Model):
    text = models.TextField()
    time = models.TimeField()
