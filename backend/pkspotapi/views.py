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

from pkspotapp.models import Spot, MyUser, Map, UserMap, Pic
from .serializers import MapSerializer, SpotSerializerD0, SpotSerializerD2, MyUserSerializerD0, MyUserSerializerD1, PicSerializer


class SpotList(APIView):
    def get(self, request, format=None):
        spots = Spot.objects.all()
        serializer = SpotSerializerD2(spots, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SpotSerializerD0(data=request.data)
        if serializer.is_valid():
            serializer.save()
            a = Map.objects.get(name='Added by me', myuser=serializer.data['adder'])
            a.spots.add(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpotDetail(APIView):
    def get_object(self, id):
        try:
            return Spot.objects.get(pk=id)
        except Spot.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        spot = self.get_object(id)
        serializer = SpotSerializerD2(spot)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        spot = self.get_object(id)
        serializer = SpotSerializer(spot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        spot = self.get_object(id)
        spot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):

    def get(self, request, id, format=None):
        mu = MyUser.objects.get(user=id)

        serializer = MyUserSerializerD1(mu, many=False)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        mu = MyUser.objects.get(pk=id)
        mu.social = request.data['social']
        mu.bio = request.data['bio']
        p = request.data.get('profile_picture', None)
        #if p:
            #os.remove(mu.profile_picture.path)
        mu.profile_picture = p
        mu.save()
        serializer = MyUserSerializerD0(mu, many=False)
        return Response(serializer.data)

    def delete(self, request, id, format=None):
        u = User.objects.get(pk=id)
        u.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
      serializer = PicSerializer(data={'name':image.name, 'image':image, 'spot':request.data['spotId']})

      if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def addUser(request):
    userId = request.data['id']
    u = User.objects.get(pk=userId)
    mu = MyUser.objects.create(user=u)
    a = Map.objects.create(name='Added by me')
    f = Map.objects.create(name='Favourites')
    muA = UserMap(user=mu, map=a, role='C')
    muF = UserMap(user=mu, map=f, role='C')
    muA.save()
    muF.save()

    serializer = MyUserSerializerD0(mu)
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
