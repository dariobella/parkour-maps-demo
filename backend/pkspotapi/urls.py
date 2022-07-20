from lib2to3.pygram import pattern_grammar
from django.urls import path, include
from . import views

urlpatterns = [

    path('api/spots/', views.spots, name="spots"),
    path('api/spotPics/<id>/', views.spotPics, name="spotPics"),
    path('api/addSpot/', views.addSpot, name="addSpot"),
    path('api/addPics/', views.addPics, name="addPics"),
    path('api/addUser/', views.addUser, name="addUser"),
    path('api/profile/<id>/', views.profile, name="profile"),
    path('api/myProfile/<id>/', views.myProfile, name="myProfile"),
    path('api/updateProfile/<id>/', views.updateProfile, name="updateProfile"),
    path('api/myMaps/<id>/', views.myMaps, name="myMaps"),
    path('api/map/<id>/', views.map, name="map"),

]
