from rest_framework import serializers
from pkspotapp.models import Users, UsersMaps, Maps, MapsSpots, Spots, Pics, AuthUser

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class UsersMapsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersMaps
        fields = '__all__'


class MapsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maps
        fields = '__all__'


class MapsSpotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapsSpots
        fields = '__all__'


class SpotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spots
        fields = '__all__'


class PicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pics
        fields = '__all__'
