import base64
import json
import datetime

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from django.forms.models import model_to_dict


from users import models
from users import serializers

from rest_auth.registration.views import RegisterView


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


class CustomRegisterView(RegisterView):
    queryset = models.User.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'put', 'delete']
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    ordering_fields = ('date_joined',)


class UserProfilesViewSet(generics.ListAPIView):
    serializer_class = serializers.UserProfileSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']
        queryset = models.UserProfile.objects.filter(user__id=user_id)

        return queryset


class ShowPdf(generics.ListAPIView):
    """
    A view that returns pdf representation of a given user.
    """
    queryset = models.User.objects.all()

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        try:
            object = models.User.objects.get(id=user_id)
            object = model_to_dict(object)
        except models.User.DoesNotExist:
            return Response({"message": "User doesn't exists for this id"})

        return Response({'message': 'ok', 'user': base64.b64encode(json.dumps(object, default=myconverter).encode('utf-8'))})



