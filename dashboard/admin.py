# -*- coding: utf-8 -*-
from django.contrib.gis import admin

from .models import Truck, Commune, Street


@admin.register(Truck)
class TruckAdmin(admin.OSMGeoAdmin):
    list_display = (
        'id',
        'obu_id',
        'measurement_date',
        'weight_category',
        'average_velocity',
        'country_code',
        'euro_value',
        'last_position',
        'route',
    )
    list_filter = ('measurement_date',)


@admin.register(Commune)
class CommuneAdmin(admin.OSMGeoAdmin):
    list_display = (
        'id',
        'name',
        'population',
        'postal_code',
        'area',
    )
    search_fields = ('name',)


@admin.register(Street)
class StreetAdmin(admin.OSMGeoAdmin):
    list_display = (
        'id',
        'name',
        'speed_limit',
        'category',
        'one_way',
        'bridge',
        'tunnel',
        'commune',
    )
    list_filter = ('bridge', 'tunnel')
    autocomplete_fields = ('commune',)
    search_fields = ('name',)


