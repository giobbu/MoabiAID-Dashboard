"""
Module that manages database acces, all requests for data should come through here
"""
from django.core.serializers import serialize

from dashboard.models import *
from .figures import *


def get_commune_data(req_data):
    """
    Handles retrieval of the data on the communes
    """
    communes = Commune.objects.all()
    print(communes)
    data = []
    if req_data == 'all':
        data = list(communes.values())
    elif req_data == 'borders':
        print('Serializing border data')
        # data = {
        #     'type': 'FeatureCollection',
        #     'crs': {
        #         'type': 'name',
        #         'properties': {'name': 'EPSG:4326'}
        #     },
        #     'features': [c.json for c in communes]
        # }
        data = serialize('geojson', communes, geometry_field='boundaries')

    # TODO: Implement retrieval of other data attributes here
    print(data)
    return data


def get_truck_data(req_data):
    trucks = Truck.objects.all()
    data = []
    if req_data == 'in_commune':
        data = trucks_in_commune_table(trucks, Commune.objects.all())

    # print(data)
    return data


def get_chart(chart_name):
    communes = Commune.objects.all()
    trucks = Truck.objects.all()

    data = []

    # print(f'retrieving chart {chart_name}')

    if chart_name == 'cat_dist':
        data = category_distribution(trucks, communes)

    # print(data)

    return data
