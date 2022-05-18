from django.db import models
from django.utils.translation import gettext_lazy as gtl

def upload_to(instance, filename):
  return 'spots/{filename}'.format(filename=filename)


class MyUser(models.Model):
    #user = models.OneToOneField(AuthUser, models.CASCADE)
    social = models.CharField(max_length=150, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'my_user'


class Spot(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=24)
    description = models.TextField(blank=True, null=True)
    adder = models.OneToOneField(MyUser, models.SET_NULL, null=True)

    class Meta:
        db_table = 'spots'