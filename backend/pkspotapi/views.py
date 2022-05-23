import re
from unicodedata import name
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from pkspotapp.models import Spot, MyUser, Map, UserMap
from .serializers import MapSerializer, SpotSerializer, MyUserSerializer

@api_view(['GET'])
def spots(request):
    spots = Spot.objects.all()
    serializer = SpotSerializer(spots, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addUser(request):
    userId = request.data['id']
    u = User.objects.get(pk=userId)
    mu = MyUser.objects.create(user=u)
    a = Map.objects.create(name='Added by me')
    f = Map.objects.create(name='Favourites')
    umA = UserMap(user=mu, map=a, role='C')
    umF = UserMap(user=mu, map=f, role='C')
    umA.save()
    umF.save()

    serializer = MyUserSerializer(mu)
    return Response(serializer.data)


@api_view(['GET'])
def myProfile(request, id):
    u = User.objects.get(pk=id)
    mu = MyUser.objects.get(user=u)

    serializer = MyUserSerializer(mu, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def myMaps(request, id):
    mu = MyUser.objects.get(pk=id)

    serializer = MapSerializer(mu.maps.all(), many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addSpot(request):

    serializer = SpotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    a = Map.objects.get(name='Added by me', myuser=serializer.data['adder'])
    a.spots.add(serializer.data['id'])

    return Response(serializer.data)
