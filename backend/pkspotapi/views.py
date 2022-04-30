from rest_framework.response import Response
from rest_framework.decorators import api_view
from pkspotapp.models import Users, Spots, Pics
from .serializers import UsersSerializer, SpotsSerializer, PicsSerializer
from rest_framework.permissions import IsAuthenticated


# ----------------- USERS --------------------------------------------


class UsersView:
    permission_classes = (IsAuthenticated,)

    @api_view(['GET'])
    def users(request):
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def selectUser(request, id):
    user = Users.objects.get(id=id)
    serializer = UsersSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def addUser(request):
    serializer = UsersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def updateUser(request, id):
    user = Users.objects.get(id=id)
    serializer = UsersSerializer(instance=user ,data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def deleteUser(request, id):
    user = Users.objects.get(id=id)
    user.delete()

    return Response(status=204)


# ----------------- SPOTS --------------------------------------------

@api_view(['GET'])
def spots(request):
    spots = Spots.objects.all()
    serializer = SpotsSerializer(spots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def selectSpot(request, id):
    spot = Spots.objects.get(id=id)
    serializer = SpotsSerializer(spot, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def addSpot(request):
    serializer = SpotsSerializer(data=request.data)

    if serializer.is_valid():
        lastSpot = serializer.save()

    return Response(lastSpot.id)


@api_view(['POST'])
def updateSpot(request, id):
    spot = Spots.objects.get(id=id)
    serializer = UsersSerializer(instance=spot ,data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def deleteSpot(request, id):
    spot = Spots.objects.get(id=id)
    spot.delete()

    return Response(status=204)


# ----------------- PICS --------------------------------------------

@api_view(['GET'])
def pics(request):
    pics = Pics.objects.all()
    serializer = PicsSerializer(pics, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addPics(request):
    images = request.FILES.getlist('images')

    n = 0
    for image in images:
      print(image)
      n += 1

    #if serializer.is_valid():
    #    serializer.save()

    return Response(n)