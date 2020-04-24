"""
Module that calls functions for real time data
"""
import json
from pathlib import Path

from shapely import geometry

from kafka import KafkaConsumer

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



STREAMING_FILES = Path('/streaming_files')
def get_rt(data):
    """
    Retrieves the real-time state of the given view (roads, communes, trucks).
    Currently only streets are supported.

    NOTE: This currently reads a file, would probably be more efficient to store the state in the cache.
    
    :param data: The real-time data to be displayed on the client.
    :type data: str
    :return: A dict to be serialized to JSON for display on the client (on the map for now)
    :rtype: dict
    """
    data_file = STREAMING_FILES / (data + '.json')
    with data_file.open('rb') as json_file:
        rt_data = json.load(json_file)

    # rt_data = get_latest_kafka(data)

    if 'street' in data and rt_data['features'][0]['geometry']['type'] == 'Polygon':
       # Convert streets to LineString if these are polygons
       for i, feature in enumerate(rt_data['features']):
           poly_street = geometry.asShape(feature['geometry'])
           coord_list = [list(tup) for tup in list(poly_street.exterior.coords)]
           rt_data['features'][i]['geometry'] =  geometry.mapping(geometry.LineString(coord_list[:-1]))

    # print(rt_data['features'][0]['geometry'])
    return rt_data