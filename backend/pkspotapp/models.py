from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def upload_spot(instance, filename):
    return 'spots/{filename}'.format(filename=filename)


def upload_profile_picture(instance, filename):
    return 'profile_pictures/{filename}'.format(filename=filename)


class MyUser(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  profile_picture = models.ImageField(_("Image"), upload_to=upload_profile_picture, blank=True, null=True)
  social = models.CharField(max_length=150, null=True)
  bio = models.TextField(blank=True, null=True)
  maps = models.ManyToManyField('Map', through='MyUserMap', related_name='myusers')

  class Meta:
    db_table = 'my_user'


class Map(models.Model):
  name = models.CharField(max_length=50)
  spots = models.ManyToManyField('Spot', blank=True)

  @property
  def creator(self):
    if self.id:
      m = Map.objects.get(pk=self.id)
      c = m.myusermap_set.get(role='C').myuser.user
      return {'id': c.id, 'username': c.username}

  class Meta:
    db_table = 'maps'


class MyUserMap(models.Model):
  ROLES = [
    ('C', 'Creator'),
    ('E', 'Editor'),
    ('V', 'Viewer'),
  ]
  myuser = models.ForeignKey(MyUser, on_delete=models.CASCADE)
  map = models.ForeignKey(Map, on_delete=models.CASCADE)
  role = models.CharField(max_length=1, choices=ROLES, default='V')

  class Meta:
    unique_together = ['myuser', 'map']
    db_table = 'myusers_maps'


class Spot(models.Model):
  SPOT_TYPES = [
    ('S', 'Spot'),
    ('P', 'Parkour Park'),
    ('G', 'Gym'),
    ('U', 'Undercover Spot'),
  ]
  lat = models.FloatField()
  lng = models.FloatField()
  name = models.CharField(max_length=50)
  type = models.CharField(max_length=1, choices=SPOT_TYPES, default='S')
  description = models.TextField(blank=True, null=True)
  adder = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)

  class Meta:
    db_table = 'spots'


class Pic(models.Model):
  name = models.CharField(max_length=50)
  image = models.ImageField(_("Image"), upload_to=upload_spot)
  spot = models.ForeignKey(Spot, on_delete=models.CASCADE)

  class Meta:
    db_table = 'pics'
