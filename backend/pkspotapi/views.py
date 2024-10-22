import os
from unicodedata import name
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from django.contrib.auth.models import User

from pkspotapp.models import Spot, MyUser, Map, MyUserMap, Pic
from .serializers import UserSerializer, MapSerializerD0, MapSerializerD3, SpotSerializerD0, SpotSerializerD2, MyUserSerializer, PicSerializer


class SpotList(APIView):
  def get(self, request):
    spots = Spot.objects.all()
    serializer = SpotSerializerD2(spots, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request):
    serializer = SpotSerializerD0(data=request.data)
    if serializer.is_valid():
      serializer.save()
      a = Map.objects.get(myusers=serializer.data['adder'], name='Added by me', myusermap__role='C')
      a.spots.add(serializer.data['id'])
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpotDetail(APIView):
  def get_object(self, id):
    try:
      return Spot.objects.get(pk=id)
    except Spot.DoesNotExist:
      raise Http404

  def get(self, request, id):
    spot = self.get_object(id)
    serializer = SpotSerializerD2(spot)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, id):
    spot = self.get_object(id)
    serializer = SpotSerializerD0(spot, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id):
    spot = self.get_object(id)
    spot.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):

  def get(self, request, id):
    u = User.objects.get(pk=id)
    mu = MyUser.objects.get(user=u)
    uSerializer = UserSerializer(u, many=False)
    muSerializer = MyUserSerializer(mu, many=False)

    r = {
        'user': uSerializer.data,
        'myuser': muSerializer.data,
    }

    return Response(r, status=status.HTTP_200_OK)

  def put(self, request, id):
    mu = MyUser.objects.get(pk=id)
    mu.social = request.data['social']
    mu.bio = request.data['bio']
    p = request.data.get('profile_picture', None)
    #if p:
      #os.remove(mu.profile_picture.path)
    mu.profile_picture = p
    mu.save()
    serializer = MyUserSerializer(mu, many=False, partial=True)
    return Response(serializer.data)

  def delete(self, request, id):
    u = User.objects.get(pk=id)
    u.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def profilePicture(request, id):
  mu = MyUser.objects.get(user=id)
  return Response(data={'profilePicture': mu.profile_picture.url}, status=status.HTTP_200_OK)


@api_view(['POST'])
def toggleFavourite(request, id):
  s = Spot.objects.get(pk=id)
  f = Map.objects.get(myusers=request.data.get('user'), name='Favourites', myusermap__role='C')

  if f.spots.filter(pk=id).exists():
    f.spots.remove(s)
  else:
    f.spots.add(s)

  return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def spotPics(request, id):
  spot = Spot.objects.get(pk=id)
  p = Pic.objects.filter(spot=spot)

  serializer = PicSerializer(p, many=True)
  return Response(serializer.data)


@api_view(['POST'])
def addPics(request):
  images = request.FILES.getlist('images')

  for image in images:
    serializer = PicSerializer(data={'name': image.name, 'image': image, 'spot': request.data['spotId']})

    if serializer.is_valid():
      serializer.save()

  return Response(serializer.data)


@api_view(['POST'])
def updateSpotPics(request, id):

  deletePics = request.POST.getlist('deletePics')
  if deletePics:
    for image in deletePics:
      p = Pic.objects.get(pk=image)
      p.delete()

  images = request.FILES.getlist('addPics')

  for image in images:
    serializer = PicSerializer(data={'name': image.name, 'image': image, 'spot': id})

    if serializer.is_valid():
      serializer.save()

  return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def addUser(request):
  userId = request.data['id']
  u = User.objects.get(pk=userId)
  mu = MyUser.objects.create(user=u)
  a = Map.objects.create(name='Added by me')
  f = Map.objects.create(name='Favourites')
  muA = MyUserMap(user=mu, map=a, role='C')
  muF = MyUserMap(user=mu, map=f, role='C')
  muA.save()
  muF.save()

  serializer = MyUserSerializer(mu)
  return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def map(request, id):
  m = Map.objects.get(pk=id)
  serializer = MapSerializerD3(m)

  return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def myMaps(request, id):
  mu = MyUser.objects.get(pk=id)

  serializer = MapSerializerD0(mu.maps.all(), many=True)
  return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def addMap(request, id):
  mu = MyUser.objects.get(pk=id)
  i = request.data.get('icon', None)

  serializer = MapSerializerD0(data={'name': request.data['name'], 'description': request.data['description'],'icon': i})
  if serializer.is_valid():
    serializer.save()
    m = Map.objects.get(pk=serializer.data['id'])
    um = MyUserMap(myuser=mu, map=m, role='C')
    um.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)

  return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateMap(request, idUser, idMap):
  m = Map.objects.get(pk=idMap)
  um = MyUserMap.objects.get(myuser=idUser, map=m)

  if um.role in ['C', 'E']:
    serializer = MapSerializerD0(m, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteMap(request, userId, mapId):
  m = Map.objects.get(pk=mapId)
  um = MyUserMap.objects.get(myuser=userId, map=m)

  if um.role == 'C':
    if m.icon:
      os.remove(m.icon.path)
    m.delete()

  else:
    um.delete()

  return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def addSpotToMap(request, id):
  m = Map.objects.get(pk=request.data['map'])
  um = MyUserMap.objects.get(myuser=id, map=m)

  if um.role in ['C', 'E']:
    m.spots.add(request.data['spot'])
    return Response(status=status.HTTP_201_CREATED)
  else:
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
def deleteSpotFromMap(request, userId, spotId, mapId):
  m = Map.objects.get(pk=mapId)
  um = MyUserMap.objects.get(myuser=userId, map=m)

  if um.role in ['C', 'E']:
    if m.spots.filter(pk=spotId).exists():
      m.spots.remove(spotId)
      return Response(status=status.HTTP_204_NO_CONTENT)
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
  else:
    return Response(status=status.HTTP_401_UNAUTHORIZED)
