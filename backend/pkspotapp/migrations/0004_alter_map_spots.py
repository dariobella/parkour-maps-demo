# Generated by Django 3.2.12 on 2022-05-23 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pkspotapp', '0003_alter_map_spots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='spots',
            field=models.ManyToManyField(blank=True, to='pkspotapp.Spot'),
        ),
    ]