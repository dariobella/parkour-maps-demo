from rest_framework import serializers
from pkspotapp.models import Spot, MyUser, Map

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