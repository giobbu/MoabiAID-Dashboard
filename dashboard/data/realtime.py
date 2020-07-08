"""
Module that calls functions for real time data

Current approach to real-time:

# The streaming pipeline writes street states to a GeoJSON file in the *streaming_files* folder
# On calls to RT street state, the cache is first checked if the state is there, we use the cached json. Otherwise, we read the file and cacghe it for later
# For communes the street state (as previously retrieved) is used to count the trucks in communes, based on the summed counts for streets in that commune
# Note yet implemented: There could also be an operation for trucks in commune in the streaming pipeline, then we can compare the two counts (tucks on streets vs total in commune)

NOTE: One pitfall is cahce invalidation. The cache needs to be invalidated on every new streaming update.
        Best solution: have the streaming pipeline write directly to the cache (Redis directly?) 
"""
import json
from pathlib import Path

from shapely import geometry

from kafka import KafkaConsumer

from django.core.cache import cache

from dashboard.data import db # For common queries that can be used in real-time computations

# from pyspark.sql import SparkSession

# spark = SparkSession \
#     .builder \
#     .master("spark://90aa18139d12:7077") \
#     .getOrCreate()
#     # Configure later
#     #.appName("mobiaid-streaming") \
#     #.config("spark.some.config.option", "some-value") \
    
# def get_state():
#     pass

#NOTE: assumes this maps to a docker volume, for local install this should point to a dir where files from the streaming pipeline are stored
STREAMING_FILES = Path('/streaming_files') 
def get_rt(data, processing=None):
    """
    Retrieves the real-time state of the given view (roads, communes, trucks).
    Currently only streets are supported.

    NOTE: This currently reads a file, would probably be more efficient to store the state in the cache.
    
    :param data: The real-time data to be displayed on the client.
    :type data: str
    :return: A dict to be serialized to JSON for display on the client (on the map for now)
    :rtype: dict
    """

    rt_data = cache.get(data)

    if rt_data is None:
        data_file = STREAMING_FILES / f'state_{data if "commune" not in data else "street"}.json' # get the right file
        with data_file.open('rb') as json_file:
            rt_data = json.load(json_file)
            cache.set(data, rt_data, 30) # 30 sec timeout for now

    # rt_data = get_latest_kafka(data)

    if 'street' in data and rt_data['features'][0]['geometry']['type'] == 'Polygon':
       # Convert streets to LineString if these are polygons
       for i, feature in enumerate(rt_data['features']):
           poly_street = geometry.asShape(feature['geometry'])
           coord_list = [list(tup) for tup in list(poly_street.exterior.coords)]
           rt_data['features'][i]['geometry'] =  geometry.mapping(geometry.LineString(coord_list[:-1]))
    
    if 'commune' in data:
        # TODO: review approach: either change or need to format street data to work with this function (or work in geojson)
        com_data = cache.get('commune_status')

        if com_data is None:
            street_counts = [{}]
            rt_data = db.get_commune_counts(rt_data)
            cache.set('commune_status', rt_data)
        else:
            rt_data = com_data
        
    if 'truck' in data and processing is not None:

        return db.get_truck_data(rt_data, processing)

    # print(rt_data)
    return rt_data