from rest_framework.decorators import action
from rest_framework.response import Response

from machine_learning.models import Label, HistImage
from machine_learning.serializers import (
    LabelSerializer,
    UserSerializer,
    GroupSerializer,
    HistImageSerializer,
)

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class LabelModelViewset(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class HistImageModelViewset(viewsets.ModelViewSet):
    queryset = HistImage.objects.all()
    serializer_class = HistImageSerializer

    @action(methods=["post"], detail=False, url_path="register-images")
    def register_images(self, request):
        hist_image_serializer = self.get_serializer()
        return Response(hist_image_serializer.data, status=status.HTTP_200_OK)
