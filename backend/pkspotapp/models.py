from django.db import models
from django.utils.translation import gettext_lazy as gtl


def upload_to(instance, filename):
  return 'spots/{filename}'.format(filename=filename)


class Maps(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'maps'


class MapsSpots(models.Model):
    mapid = models.IntegerField(db_column='mapId', primary_key=True)  # Field name made lowercase.
    spotid = models.IntegerField(db_column='spotId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'maps_spots'
        unique_together = (('mapid', 'spotid'),)


class Pics(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(gtl("Image"), upload_to=upload_to)
    spotid = models.IntegerField(db_column='spotId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pics'


class Spots(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=24)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spots'


class Users(models.Model):
    username = models.CharField(unique=True, max_length=50)
    psw = models.CharField(max_length=50)
    social = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UsersMaps(models.Model):
    userid = models.IntegerField(db_column='userId', primary_key=True)  # Field name made lowercase.
    mapid = models.IntegerField(db_column='mapId')  # Field name made lowercase.
    role = models.CharField(max_length=21)

    class Meta:
        managed = False
        db_table = 'users_maps'
        unique_together = (('userid', 'mapid'),)
