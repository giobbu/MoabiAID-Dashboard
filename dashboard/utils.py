import json

import geopandas

from django import forms
from django.forms.widgets import ChoiceWidget
from django.db import connection
from django.apps import apps

from django.contrib.gis.geos import GEOSGeometry

from bootstrap_datepicker_plus import DatePickerInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field

from django_select2.forms import ModelSelect2Widget

class BadRequestError(Exception):
    """
    Simple error which indicates that a request sent to a view was not properly formatted
    """
    pass

class SliderWidget(ChoiceWidget):
    """
    Widget used with a Choice form field with a slider to select choices instead of the usual dropdown
    Uses Bootstrap custom range: https://getbootstrap.com/docs/4.1/components/forms/#range
    """

    input_type = 'range'
    template_name = 'dashboard/widgets/rangeslider.html'
    option_template_name = 'dashboard/widgets/slideroption.html'

    def __init__(self, attrs=None, min_range=0, max_range=100, step=1):
        """
        Creates a Slider widget based on a given minimum and maximum value. Step size can alos be provided
        
        :param attrs: Additional HTML attributes next to thew ones used to make a range slider (see Django docs for more info), defaults to None
        :type attrs: dict, optional
        :param min_range: Starting value of the range, defaults to 0
        :type min_range: int, optional
        :param max_range: Ending value of the range, defaults to 100
        :type max_range: int, optional
        :param step: Step size, defaults to 1
        :type step: int, optional
        :raises ValueError: If the start value of the range is larger than the end value
        """

        if max_range <= min_range:
            raise ValueError('The minimal value can not be larger than the maximal value')

        slider_attrs = {
            'class': 'custom-range',
            'min': min_range,
            'max': max_range,
            'step': step
        }

        choices = [(c,c) for c in range(min_range, max_range + step, step)] #We add to max_range to also include the max bound

        if attrs is not None:
            slider_attrs.update(attrs)
        super().__init__(attrs=slider_attrs, choices=choices)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context


class SliderField(forms.ChoiceField):
    """
    Custom Django ChoiceField that uses the slider widget
    """
    
    def __init__(self, min_range=0, max_range=100, step=1):
        widget = SliderWidget(min_range=min_range, max_range=max_range, step=step)
        super().__init__(choices=widget.choices, widget=widget)


class MapControls(forms.Form):
    """
    Controls that are used to select a date and a time for the map
    """
    date = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y')) 
    day_of_week = SliderField(min_range=1, max_range=7)
    time_of_day = SliderField(max_range=24) #Hours start at 0, the default

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_media = False
        self.helper.layout = Layout(
            Field('date'),
            Field('day_of_week', data_valuedisplay='#day_of_week_val'),
            HTML('<p id="day_of_week_val"></p>'),
            Field('time_of_day', data_valuedisplay='#time_of_day_val'),
            HTML('<p id="time_of_day_val"></p>')
        )

class StreetAnalyticControls(forms.Form):
    """
    Controls that are used for analysing street related data when a user choses to analyse by street.
    """
    street = forms.ChoiceField(
        widget=ModelSelect2Widget(
            model=apps.get_model('dashboard', 'Street'), 
            search_fields=['name', 'category']
        )
    )
    # TODO: additional controls

def get_analytic_controls(entity):
    """
    Retreives the appropriate controls when a user selects an entity to analyse (street, commune, trucks).
    
    :param entity: The chosen entity.
    :type entity: str
    :return: Appropriate control form for rendereing in the template page.
    :rtype: ~django.forms.Form
    """
    
    if entity == 'streets':
        return StreetAnalyticControls()

def get_table_as_geopandas(table, geom_name):
    """
    Utility to retrieve a GeoPandas DataFrame directly from a table in the PostGIS database
    
    :param table: name of the table in PostGIs (typically: Lowercase name of the model with 'dashboard_' in front)
    :type table: str
    :param geom_name: Name of the Geometry column for the table
    :type geom_name: str
    :return: The database table as a Geopandas Dataframe
    :rtype: ~geopandas.GeoDataFrame
    """
    return geopandas.read_postgis(f'select * from {table}', connection, geom_name) #TODO: verify that this is safe against SQL injection

def load_feature_collection(feature_dict):
    """
    Given a dict that was loaded from a geojson FeatureCollection file,
    creat geometries into GeosGeometry instances.

    :param feature_dict: feature collection loaded into a dict
    :type feature_dict: dict
    :return: lsit of tuples with the geometry turned into a GeosGeometry instance in first element and properties in the second
    :rtype: tuple(~django.contrib.gis.geos.GEOSGeometry, dict)
    """

    feature_list = []
    
    for feat in feature_dict['features']:
        geos = GEOSGeometry(json.dumps(feat['geometry']))
        feature_list.append((geos, feat['properties']))
    
    return feature_list

def get_current_values(prop_dict):
    cur_time = prop_dict['current_time']
    flow = prop_dict['list_table']['flow'] 

    first_nonzero = False

    for key, val in flow.items(): 
        if first_nonzero and val == 0.0: 
            # print(key)
            cur_key = str(int(key)-1) 
            break 
        elif not first_nonzero and val != 0.0: 
            first_nonzero = True 
    
    return {
        'flow': flow[cur_key],
        'vel': prop_dict['list_table']['vel'][cur_key]
    }

def get_time_intervals(resolution):
    """
    Returns a list of values for a given interval of time at the resquested resolution
    e.g. time_of_day means 1 hour intervals, and 24h for a full day. So a list from 0 to 24

    :param resolution: The string for a supported resolution of the time interval
    :type resolution: str
    :raises ValueError: When an invalid resolution string is provided
    :return: list of  values for the requested resolution
    :rtype: list(int)
    """
    
    # Compute batch intervals based on resolution
    if resolution == 'time_of_day':
        time_intervals = range(24)
    elif resolution == '10min_hour':
        time_intervals = range(6)
    elif resolution == 'day_of_week':
        time_intervals = range(1,8) # days start at 1
    # TODO: add any resolutions we want to support
    else:
        raise ValueError(f'{resolution} is not a valid resolution parameter')

    return time_intervals
    
