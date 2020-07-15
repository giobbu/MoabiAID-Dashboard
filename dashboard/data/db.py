"""
Module that manages database acces, all requests for data should come through here
"""
import json
import glob
import os

# Used to generate testing data, can be removed in production
import random

from pathlib import Path

from django.core.serializers import serialize
from django.db.models import Q

from dashboard.models import *
from .figures import *
from dashboard.utils import load_feature_collection, get_current_values
from mobiaid.settings import BASE_DIR


def get_commune_data(req_data):
    """
    Handles retrieval from the database of the data related to communes
    
    :param req_data: Specifies the type of data to retreive (e.g. just the commune borders or everythin that is stored in the database)
    :type req_data: str
    :return: The data on all communes in the database, either as a list of dictionaries or a geojson formatted string
    :rtype: str or list(dict)
    """
    communes = Commune.objects.all()
    # print(communes)
    data = []
    if req_data == 'all':
        data = list(communes.values())
    elif req_data == 'borders':
        # print('Serializing border data')
        # data = {
        #     'type': 'FeatureCollection',
        #     'crs': {
        #         'type': 'name',
        #         'properties': {'name': 'EPSG:4326'}
        #     },
        #     'features': [c.json for c in communes]
        # }
        data = serialize('geojson', communes, geometry_field='boundaries')


    # NOTE: Implement retrieval of other data attributes here
    # print(data)
    return data


def get_truck_data(trucks, req_data):
    """
    Retrieves the requested data related to trucks from the database for display in a `Datatables <https://datatables.net/>`_ table.
    
    :param req_data: The type of data on trucks that is requested
    :type req_data: str
    :return: The requested data on trucks (e.g. A dict that is used to created a table describing the trucks in a commune)
    :rtype: dict
    """
    truck_list = load_feature_collection(trucks)
    # print(truck_list[0])
    data = []
    if req_data == 'in_commune':
        data = trucks_in_commune_table(truck_list, Commune.objects.all())
    elif req_data == 'positions':
        data = trucks

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
    elif chart_name == 'time_counts':
        #TODO: for testing where to retrieve this?
        tod_counts = [25, 58, 79, 145, 489, 569, 896, 999, 1569, 1469, 1369, 1269, 956, 684, 598, 689, 569, 423, 852, 123, 256, 65, 48, 23] 
        data = time_of_day_distribution(tod_counts)
    elif chart_name == 'delay_distribution':
        test_delays = [random.randint(0,30) for i in range(24)]
        data = delay_distribution(test_delays)

    # print(data)

    return data

def get_typical_traffic(aggregation_lvl, value='mean_flow'):

    # Extract aggregate function and requested measure
    aggregate_fun, measure = value.split('_')

    typical_values = {}
    if aggregation_lvl == 'Commune':
        instances = Commune.objects.all()
    elif aggregation_lvl == 'Street':
        instances = Street.objects.all()
    elif aggregation_lvl == 'Trucks':
        pass # TODO: this might require a different approach
    else:
        raise ValueError(f'{aggregation_lvl} is not a valid aggregation level for typical traffic.')

    for inst in instances:
        # TODO: depending on the final format, this might need to be modified
        typical_values[inst.name] = inst.typical_values[aggregate_fun][measure]

    return typical_values

# Functions that require more context for the request

def get_commune_counts(street_counts):
    """
    Computes the number of trucks in each commune based on the number of trucks on each street.

    :param street_counts: A dictionary containing every processed street with the number of trucks for each
    :type street_counts: dict   
    :return: The number of trucks in each commune
    :rtype: dict
    """

    communes = Commune.objects.all().prefetch_related('streets')

    # Serialize communes and deserialize back to dict
    com_features = json.loads(serialize('geojson', communes, geometry_field='boundaries', fields=('name',)))
    # print(type(com_features))
    streets = load_feature_collection(street_counts)

    # print(street_counts['features'][0])

    # Get counts for each street in every commune
    for idx, com in enumerate(communes):
        # streets = com.streets.all()
        # print(com)

        n_trucks_commune = 0

        for i, (street, props) in enumerate(streets):
            # street can be a name or a database id
            # if streets.filter(Q(name__icontains=street) | Q(pk=street)).exists():
            if com.boundaries.contains(street):
                cur_vals = get_current_values(props)
                n_trucks_commune += cur_vals['flow']
                # pop from list to have less items on next commune iteration
                streets.pop(i)
        
        # This works because the ordering in the feauture list should be preserved from the queryset
        com_features['features'][idx]['properties']['total'] = n_trucks_commune
    
    # print(com_features)
    return com_features

def get_layers(req_layers):
    
    layers = []

    if req_layers == 'areas_of_interest':
        layers_dir = os.path.join(BASE_DIR, 'dashboard/static/dashboard/json/Layers/')
        area_files = glob.glob(layers_dir + '*.geojson')
        print(area_files)
        for layer_fname in area_files:
            with open(layer_fname, 'r') as layer_file:
                features = json.load(layer_file)
                features['layer_name'] = Path(layer_fname).stem
                layers.append(features)
    
    print(layers)
    return layers

