"""
Module that handles incoming data requests related to a certain view and delegates to the appropriate submodules 
"""
from .db import *

def get_data(table, req_data):
    """
    Handles retrieval of data on any database entity
    """
    
    if table == 'Commune':
        data = get_commune_data(req_data)
    if table == 'Truck':
        data = get_truck_data(req_data)

    return data