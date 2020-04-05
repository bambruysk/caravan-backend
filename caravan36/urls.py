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
from django.conf.urls.static import static
from django.views.generic import TemplateView

from caravan36 import settings
from caravan_routes import views
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from caravan_routes.views import GeoPointsView, GeoPointsCreateView, ListGeopointsView, RoutePointsListView, \
    RouteListView
from caravan_routes.routers import router

urlpatterns = \
    [
        path('admin/', admin.site.urls),
        path('geopoints/', GeoPointsView.as_view()),
        path('api/geopoints/create', GeoPointsCreateView.as_view(), name='add_geopoint'),
        path('update/', views.update, name='update_db_json'),
        url(r'api-auth/', include('rest_framework.urls')),
        path('auth/', views.ExampleView.as_view(), name="auth"),
        path('auth-token/', views.CustomAuthToken.as_view(), name="auth-token"),
        path('api/auth-token/', views.CustomAuthToken.as_view(), name="auth-token"),
        path('change_passwd/', views.ChangePasswordView.as_view(), name="change_passwd"),
        url(r'^api/', include((router.urls))),
        path('', TemplateView.as_view(template_name="caravan_routes/main_page.html",
                                      extra_context={'router_urls': router.get_urls()})),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
