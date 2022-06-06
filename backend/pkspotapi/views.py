import re
from unicodedata import name
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from pkspotapp.models import Spot, MyUser, Map, UserMap
from .serializers import MapSerializer, SpotSerializer, MyUserSerializer, PicSerializer

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

@api_view(['PUT'])
def updateProfile(request, id):
    mu = MyUser.objects.get(pk=id)
    mu.social = request.data['social']
    mu.bio = request.data['bio']
    mu.profile_picture = request.data.get('profile_picture', None)
    mu.save()
    serializer = MyUserSerializer(mu, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def myMaps(request, id):
    mu = MyUser.objects.get(pk=id)

    serializer = MapSerializer(mu.maps.all(), many=True)
    return Response(serializer.data)

@api_view(['GET'])
def map(request, id):
    m = Map.objects.get(pk=id)

    serializer = MapSerializer(m)
    return Response(serializer.data)


@api_view(['POST'])
def addSpot(request):

    serializer = SpotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    a = Map.objects.get(name='Added by me', myuser=serializer.data['adder'])
    a.spots.add(serializer.data['id'])

    return Response(serializer.data)


@api_view(['POST'])
def addPics(request):
    images = request.FILES.getlist('images')

    for image in images:
      serializer = PicSerializer(data={'name':image.name, 'image':image, 'spot':request.data['spotId']})

      if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
