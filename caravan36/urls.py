"""caravan36 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from caravan_routes import views
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


from caravan_routes.views import GeoPointsView, GeoPointsCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('geopoints/', GeoPointsView.as_view()),
    path('geopoints/create', GeoPointsCreateView.as_view(), name='add_geopoint'),
    path('update/', views.update, name='update_db_json'),
    url(r'^api-auth/', include('rest_framework.urls'))

]



