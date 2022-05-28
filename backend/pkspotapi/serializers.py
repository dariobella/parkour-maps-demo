from rest_framework import serializers
from pkspotapp.models import Spot, MyUser, Map, Pic

class SpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = '__all__'


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'


class PicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pic
        fields = '__all__'