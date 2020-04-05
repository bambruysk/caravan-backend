from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from caravan_routes.models import GeoPoint, Route, RoutePoint
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, JsonResponse

# REST
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .serializers import ChangePasswordSerializer, GeoPointSerializer, RoutePointSerializer, RouteSerializer, \
    CurrentStateSerializer


# Create your views here.


class GeoPointsView(ListView):
    model = GeoPoint
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)




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

#
# def check_version(req  ):
#     version = req.GET.get("version",0)
#     #
#     last_route_coll = RouteCollection.objects.all().order_by(version)[:1]
#     if last_route_coll.version > version:
#         return HttpResponse("UPDATE")
#     else:
#         return HttpResponse("OK")


def update (req):
    routes = Route.objects.all()
    return JsonResponse(routes)


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user).encode('utf-8'),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth).encode('utf-8'),  # None
        }
        return Response(content)

    def post(self):
        pass

## Authorization
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class CreateNewUser(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user = self.create(request)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        print(request)
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListGeopointsView(ListAPIView):
    serializer_class = GeoPointSerializer
    model = GeoPoint
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = GeoPoint.objects.all()


class GeoPointsCreateView(CreateAPIView):
    serializer_class = GeoPointSerializer
    model = GeoPoint
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



class RoutePointsListView(ListAPIView):
    serializer_class = RoutePointSerializer
    model = RoutePoint
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RoutePoint.objects.all()


class RouteListView(ListAPIView):
    serializer_class = RouteSerializer
    model = Route
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Route.objects.all()


class CurrentStateView(UpdateAPIView):
    serializer_class = CurrentStateSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def update(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():

    # TODO: Реализовать обновление состояние караванов
