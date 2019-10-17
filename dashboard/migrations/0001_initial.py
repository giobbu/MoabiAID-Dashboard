# Generated by Django 2.2 on 2019-06-07 15:30

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('population', models.PositiveIntegerField()),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('boundaries', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('speed_limit', models.PositiveSmallIntegerField()),
                ('path', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='TrafficEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resolved', models.BooleanField(default=False)),
                ('report_time', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('position', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obu_id', models.PositiveSmallIntegerField()),
                ('measurement_date', models.DateField()),
                ('weight_category', models.PositiveSmallIntegerField()),
                ('average_velocity', models.FloatField()),
                ('country_code', models.CharField(max_length=3)),
                ('euro_value', models.PositiveSmallIntegerField()),
                ('last_position', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('route', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
            ],
        ),
    ]