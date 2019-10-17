"""
Module that handles incoming data requests related to a certain view and delegates to the appropriate submodules 
"""
from .db import *
from .realtime import get_rt
from dashboard.utils import BadRequestError

def get_data(table, req_data, usage):
    """
    Handles retrieval of data on any database entity
    """

    data = []

    if usage is None:
        if table == 'Commune':
            data = get_commune_data(req_data)
        elif table == 'Truck':
            data = get_truck_data(req_data)

    elif usage == 'chart':
        data = get_chart(req_data) #TODO finish chart data requests
    elif usage == 'real-time':
        data = get_rt(table)
    else:
        raise BadRequestError(f'At least one of the provided request parameters (data_usage: {usage}, table: {table}, data: {req_data}) is invalid')

    return data