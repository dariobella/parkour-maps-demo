from rest_framework import serializers
from django.contrib.auth.models import User
from pkspotapp.models import Spot, MyUser, Map, Pic


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MyUserSerializerD0(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['id', 'profile_picture', 'social', 'bio', 'maps']
        depth = 0


class MyUserSerializerD1(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['id', 'profile_picture', 'social', 'bio', 'maps']
        depth = 1


class SpotSerializerD0(serializers.ModelSerializer):

    class Meta:
        model = Spot
        fields = ['id', 'lat', 'lng', 'name', 'type', 'description', 'adder']
        depth = 0


class SpotSerializerD2(serializers.ModelSerializer):

    class Meta:
        model = Spot
        fields = ['id', 'lat', 'lng', 'name', 'type', 'description', 'adder']
        depth = 2


class MapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Map
        fields = ['id', 'name', 'spots']
        depth = 3


class PicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pic
        fields = ['id', 'name', 'image', 'spot']