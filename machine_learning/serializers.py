from machine_learning.models import Label, HistImage

from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"


class HistImageSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(use_url=False)

    class Meta:
        model = HistImage
        fields = ("file", "label", "magnification", "stain")
