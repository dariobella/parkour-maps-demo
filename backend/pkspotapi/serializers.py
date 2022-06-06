from rest_framework import serializers
from pkspotapp.models import Spot, MyUser, Map, Pic

class SpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = ['id', 'lat', 'lng', 'name', 'type', 'description', 'adder']


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'user', 'profile_picture', 'social', 'bio', 'maps']


class MapSerializer(serializers.ModelSerializer):
    spots = SpotSerializer(many=True, read_only=True)

    class Meta:
        model = Map
        fields = ['id' ,'name', 'spots']


class PicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pic
        fields = ['id', 'name', 'image', 'spot']