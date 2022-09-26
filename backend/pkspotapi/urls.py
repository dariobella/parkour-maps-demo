from lib2to3.pygram import pattern_grammar
from django.urls import path, include
from . import views

urlpatterns = [

    path('api/spots/', views.SpotList.as_view(), name="spotList"),
    path('api/spots/<int:id>/', views.SpotDetail.as_view(), name="spotDetail"),
    path('api/toggleFavourite/<int:id>/', views.toggleFavourite, name="toggleFavourite"),
    path('api/spotPics/<int:id>/', views.spotPics, name="spotPics"),
    path('api/addPics/', views.addPics, name="addPics"),
    path('api/updateSpotPics/<int:id>/', views.updateSpotPics, name="updateSpotPics"),
    path('api/addUser/', views.addUser, name="addUser"),
    path('api/user/<int:id>/', views.UserDetail.as_view(), name="userDetail"),
    path('api/profilePicture/<int:id>/', views.profilePicture, name="profilePicture"),
    path('api/myMaps/<int:id>/', views.myMaps, name="myMaps"),
    path('api/map/<int:id>/', views.map, name="map"),
    path('api/addMap/<int:id>/', views.addMap, name="addMap"),
    path('api/updateMap/<int:idUser>/<int:idMap>/', views.updateMap, name="updateMap"),
    path('api/deleteMap/<int:userId>/<int:mapId>', views.deleteMap, name="deleteMap"),
    path('api/addSpotToMap/<int:id>/', views.addSpotToMap, name="addSpotToMap"),
    path('api/deleteSpotFromMap/<int:userId>/<int:spotId>/<int:mapId>/', views.deleteSpotFromMap, name="deleteSpotFromMap"),

]



