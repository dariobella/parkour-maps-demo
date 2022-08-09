from lib2to3.pygram import pattern_grammar
from django.urls import path, include
from . import views


urlpatterns = [

    path('api/spots/', views.spots, name="spots"),
    path('api/spotPics/<int:id>/', views.spotPics, name="spotPics"),
    path('api/addSpot/', views.addSpot, name="addSpot"),
    path('api/updateSpot/<int:id>/', views.updateSpot, name="updateSpot"),
    path('api/addPics/', views.addPics, name="addPics"),
    path('api/addUser/', views.addUser, name="addUser"),
    path('api/profile/<int:id>/', views.profile, name="profile"),
    path('api/updateProfile/<int:id>/', views.updateProfile, name="updateProfile"),
    path('api/myMaps/<int:id>/', views.myMaps, name="myMaps"),
    path('api/map/<int:id>/', views.map, name="map"),

]
