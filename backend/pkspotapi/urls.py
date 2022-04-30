from django.urls import path, include
from . import views
#from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    #path('api/token/', TokenObtainPairView.as_view()),
    #path('api/token-refresh/', TokenRefreshView.as_view()),

    path('api/users/', views.UsersView.users, name="users"),
    path('api/selectUser/<str:id>/', views.selectUser, name="selectUser"),
    path('api/addUser/', views.addUser, name="addUser"),
    path('api/updateUser/<str:id>/', views.updateUser, name="updateUser"),
    path('api/deleteUser/<str:id>/', views.deleteUser, name="deleteUser"),

    path('api/spots/', views.spots, name="spots"),
    path('api/selectSpot/<str:id>/', views.selectSpot, name="selectSpot"),
    path('api/addSpot/', views.addSpot, name="addSpot"),
    path('api/updateSpot/<str:id>/', views.updateSpot, name="updateSpot"),
    path('api/deleteSpot/<str:id>/', views.deleteSpot, name="deleteSpot"),

    path('api/pics/', views.pics, name="pics"),
    path('api/addPics/', views.addPics, name="addPics"),


]
