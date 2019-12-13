"""
Module that manages database acces, all requests for data should come through here
"""
from django.core.serializers import serialize

from dashboard.models import *
from .figures import *


def get_commune_data(req_data):
    """
    Handles retrieval from the database of the data related to communes
    
    :param req_data: Specifies the type of data to retreive (e.g. just the commune borders or everythin that is stored in the database)
    :type req_data: str
    :return: The data on all communes in the database, either as a list of dictionaries or a geojson formatted string
    :rtype: str or list(dict)
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
    """
    Retrieves the requested data related to trucks from the database
    
    :param req_data: The type of data on trucks that is requested
    :type req_data: str
    :return: The requested data on trucks (e.g. A dict that is used to created a table describing the trucks in a commune)
    :rtype: dict
    """
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
