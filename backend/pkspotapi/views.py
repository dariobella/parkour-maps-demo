import re
from rest_framework.response import Response
from rest_framework.decorators import api_view
import jsonpickle
#jsonpickle.encode(obj)

from django.contrib.auth.models import User

from pkspotapp.models import Spot, MyUser, Map
from .serializers import SpotSerializer

@api_view(['GET'])
def spots(request):
    spots = Spot.objects.all()
    serializer = SpotSerializer(spots, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addUser(request):
    userId = request.data['id']
    u = User.objects.get(pk=userId)
    mu = MyUser(user=u)
    a = Map(name='Added by me')
    f = Map(name='favourites')
    mu.maps.add(a, f)
    mu.save

    return Response(jsonpickle.encode(mu))
