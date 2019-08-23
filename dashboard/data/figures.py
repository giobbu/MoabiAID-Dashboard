def trucks_in_commune_table(trucks, communes):
    result = {
        'total_trucks': trucks.count(),
        'cat_b': 0,
        'cat_c': 0,
        'table': {
            'data': [],
            'columns': [
                {'data': 'commune'},
                {'data': 'total'},
                {'data': 'cat_b'},
                {'data': 'cat_c'}
            ],
            # Options
            'searching': False,
            'paging': False,
            'info': False
        }
    }
    for com in communes:
        boundaries = com.boundaries
        #NOTE: IMPORTANT! As a placeholder we use the truck's last position. For the real deal this should use RT data or the position at a certain time
        trucks_here = trucks.filter(last_position__within=boundaries) 
        commune_data = {
            'commune': com.name,
            'total': trucks_here.count(),
            'cat_b': 0,
            'cat_c': 0
        }

        for th in trucks_here:
            truck_mam = th.weight_category
            if truck_mam > 3500:
                commune_data['cat_c'] += 1
            else:
                commune_data['cat_b'] += 1
        
        result['cat_b'] += commune_data['cat_b']
        result['cat_c'] += commune_data['cat_c']
        result['table']['data'].append(commune_data)
    
    return result

def make_category_series(s_type, category, value, name=None, columns=None):
    """
    Utility function that constructs a dictionary that is formatted according to what is expected for 
    an amCharts series that supports categories (i.e. the chart has a CategoryAxis for its x-axis).
    In this case it means that the dataFields property has valueY and categoryX properties.
    Currently only tested with column series.
    
    :param s_type: The concrete type of series that supports a categorical x-axis
    :type s_type: str
    :param category: Name of the category propertye in the data
    :type category: str
    :param value: Name of the value property in the data
    :type value: str
    :param name: The name of this series, defaults to None
    :type name: str, optional
    :param columns: description of the chart columns (`details <https://www.amcharts.com/docs/v4/reference/column/>`_), defaults to None
    :type columns: list(dict), optional
    :return: The series configuration
    :rtype: dict
    """

    series = {
        'type': s_type,
        'dataFields': {
            'valueY': value,
            'categoryX': category
        }
    }
    
    if name is not None:
        series['name'] = name

    if columns is not None:
        series['columns'] = columns

    return series


def bar_chart(data, name, category, value, xlabel=None, ylabel=None):
    """
    Constructs a dictionary to be passed as the configuration for a bar charts in amCharts
    
    :param data: A list of dictionaries representing the data we want to display
    :type data: list(dict)
    :param name: Name to be passed to the series
    :type name: str
    :param category: Name of the category key in the data dictionary
    :type category: str
    :param value: Name of the value key in the data dictionary
    :type value: str
    :param xlabel: Label for the x-axis, defaults to None
    :type xlabel: str, optional
    :param ylabel: Label for the y-axis, defaults to None
    :type ylabel: str, optional
    :return: Dictionary that is formatted for client-side configuration of an amCharts barchart
    :rtype: dict
    """

    x_axis = {
        'type': 'CategoryAxis',
        'dataFields': {
            'category': category
            }
    }

    if xlabel is not None:
        x_axis['dataFields']['title'] = {'text': xlabel} 

    y_axis = {
        'type': 'ValueAxis'
    }

    if ylabel is not None:
        y_axis['title']['text'] = ylabel

    columns = {
        'tooltipText': '{categoryX}: {valueY}'
        #Note: further customization of table should happen client-side
        }
        
    series = make_category_series('ColumnSeries', category, value, name, columns)

    chart_dict = {
        'data': data,
        'xAxes': [x_axis], # We assume only one x and y axis for this type of chart
        'yAxes': [y_axis],
        'series': [series],
        'type': 'XYChart'
    }

    return chart_dict

def clustered_bar_chart(data, category, values):
    """
    Cosntructs a dictionary that describes the configuration of a clustered barchart in amCharts
    
    :param data: A list of dictionaries representing the data we want to display
    :type data: list(dict)
    :param category: Name of the category key in the data dictionary
    :type category: str
    :param values: Name of the value keys for the different columns in the data dictionary
    :type values: list(str)
    :return: dictionary describing the configuration as expected by amCharts
    :rtype: dict
    """

    x_axis = {
        'type': 'ValueAxis',
        'renderer': {
            'opposite' : True # To display values on top of the chart instead of bottom
        }
    }

    y_axis = {
        'type': 'CategoryAxis',
        'dataFields': {
            'category': category
        },
        # Format to get a nice layout
        'renderer': {
            'grid': {
                'template': {
                    'location': 0
                }
            },
            'cellStartLocation': 0.1,
            'cellEndLocation': 0.9
        }
    }

    series = []
    for val in values:
        # Can not use factory as x and y are reversed
        ser = {
            'type': 'ColumnSeries',
            'dataFields': {
                'valueX': val,
                'categoryY': category
            },
            'name': val[2:].capitalize(),
            'columns': {
                'template': {
                    'tooltipText': "{name}: {valueX}",
                    'height': "90%"
                }
            }
        }

        series.append(ser)

    chart_dict = {
        'data': data,
        # Note: Add this property containing the following function to client-side JS for ordered bars: 
        # events: {beforedatavalidated: function(ev) {ev.target.data.sort(function(a, b) {return a.n_variants - b.n_variants;});}},
        'xAxes': [x_axis], # We assume only one x and y axis for this type of chart
        'yAxes': [y_axis],
        'series': series,
        'legend': {
            'type': "Legend"
        },
        'type': 'XYChart'
    }

    return chart_dict

def category_distribution(trucks, communes):

    data = []

    for com in communes:
        boundaries = com.boundaries
        #NOTE: IMPORTANT! As a placeholder we use the truck's last position. For the real deal this should use RT data or the position at a certain time
        trucks_here = trucks.filter(last_position__within=boundaries) 
        commune_data = {
            'commune': com.name,
            'cat_b': 0,
            'cat_c': 0
        }

        for th in trucks_here:
            truck_mam = th.weight_category
            if truck_mam > 3500:
                commune_data['cat_c'] += 1
            else:
                commune_data['cat_b'] += 1
        
        data.append(commune_data)

    return clustered_bar_chart(data, 'commune', ['cat_a', 'cat_b'])