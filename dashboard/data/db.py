"""
Module that manages database acces, all requests for data should come through here
"""
from dashboard.models import *

def get_commune_data(req_data):
    """
    Handles retrieval of the data on the communes
    """
    communes = Commune.objects.all()
    data = []
    if req_data == 'all':
        data = list(communes.values())
    elif req_data == 'borders':
        for c in communes:
            data.append(c.get_boundaries())

    #TODO: Implement retrieval of other data attributes here

    return data