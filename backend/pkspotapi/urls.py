from lib2to3.pygram import pattern_grammar
from django.urls import path, include
from . import views


urlpatterns = [

    path('api/spots/', views.SpotList.as_view(), name="spotList"),
    path('api/spots/<int:id>/', views.SpotDetail.as_view(), name="spotDetail"),
    path('api/spotPics/<int:id>/', views.spotPics, name="spotPics"),
    path('api/addPics/', views.addPics, name="addPics"),
    path('api/updateSpotPics/<int:id>/', views.updateSpotPics, name="updateSpotPics"),
    path('api/addUser/', views.addUser, name="addUser"),
    path('api/user/<int:id>/', views.UserDetail.as_view(), name="userDetail"),
    path('api/myMaps/<int:id>/', views.myMaps, name="myMaps"),
    path('api/map/<int:id>/', views.map, name="map"),

]
