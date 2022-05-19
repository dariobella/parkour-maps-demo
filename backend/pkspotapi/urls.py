from django.urls import path, include
from . import views

urlpatterns = [

    path('api/spots/', views.spots, name="spots"),


]
