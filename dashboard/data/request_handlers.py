"""
Module that handles incoming data requests related to a certain view and delegates to the appropriate submodules 
"""
from .db import *
from .realtime import get_rt
from dashboard.utils import BadRequestError

def get_data(table, req_data, usage):
    """
    Handles retrieval of data on any database entity
    
    :param table: the database table (i.e. the type of entity) to query
    :type table: str
    :param req_data: the type of data to retrieve related to the given entity
    :type req_data: str
    :param usage: What the requested data will be used for (e.g. constructing a table or generating a figure)
    :type usage: str
    :raises BadRequestError: If the request parameters are invalid
    :return: The data that was requested, formatted according to usage
    :rtype: str or dict or list(dict)
    """

    print('Data request:')
    print(table, req_data, usage)
    data = []

    if usage is None:
        if table == 'Commune':
            data = get_commune_data(req_data)
        # elif table == 'Truck':
        #     data = get_truck_data(req_data)

    elif usage == 'chart':
        # The data is a formatted chart
        data = get_chart(req_data)
    elif usage == 'real-time':
        # Real time state of requested entity
        data = get_rt(table, req_data)
    elif usage == 'typical':
        # Typical state(s) for requested entity
        data = get_typical_traffic(, req_data)
    elif usage == 'layers':
        data = get_layers(req_data)
    else:
        raise BadRequestError(f'At least one of the provided request parameters (data_usage: {usage}, table: {table}, data: {req_data}) is invalid')

    return data