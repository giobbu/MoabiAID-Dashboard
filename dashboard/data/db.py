"""
Module that manages database acces, all requests for data should come through here
"""
from django.core.serializers import serialize
from django.db.models import Q

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
    Retrieves the requested data related to trucks from the database for display in a `Datatables <https://datatables.net/>`_ table.
    
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
    """
    Retrieves data for the given chart and formats it for use with the `AmCharts <https://www.amcharts.com/>`_ library.
    
    :param chart_name: The name of the chart to retrieve.
    :type chart_name: str
    :return: Formatted dictionary for instantiating an AmCharts chart on the client. Already contains necessary data.
    :rtype: dict or list
    """
    communes = Commune.objects.all()
    trucks = Truck.objects.all()

    data = []

    # print(f'retrieving chart {chart_name}')

    if chart_name == 'cat_dist':
        data = category_distribution(trucks, communes)

    # print(data)

    return data

def get_typical_traffic(aggregation_lvl):
    pass #TODO: retrieve typical traffic data given the level of aggrgation: Commune, Street, Truck (clusters where trucks are typically located)

# Functions that require more context for the request

def get_commune_counts(street_counts):
    """
    Computes the number of trucks in each commune based on the number of trucks on each street.

    :param street_counts: A dictionary containing every processed street with the number of trucks for each
    :type street_counts: dict   
    :return: The number of trucks in each commune
    :rtype: dict
    """

    communes = Commune.objects.all()

    com_counts = {}

    # Get counts for each street in every commune
    for com in communes:
        streets = com.streets

        n_trucks_commune = 0

        for street, n_trucks in street_counts.items():
            # street can be a name or a database id
            if streets.filter(Q(name__icontains=street) | Q(pk=street)).exists():
                n_trucks_commune += street_counts.pop(street) # pop from dict to have less items on next commune iteration
        
        com_counts[com.name] = n_trucks_commune
    
    return com_counts

