import numpy as np
from scipy.stats import norm

from dashboard.utils import get_time_intervals

##########
# Tables #
##########


def trucks_in_commune_table(trucks, communes):
    """
    Generates a dictionary that is formatted as to generate a DataTables table on the client.
    This table contains the counts of trucks in each commune

    :param trucks: List of trucks that where retrieved from the database
    :type trucks: ~django.db.models.query.QuerySet
    :param communes: List of communes that are stored in the database
    :type communes: ~django.db.models.query.QuerySet
    :return: Formatted dictionary for DataTables
    :rtype: dict
    """
    result = {
        'total_trucks': len(trucks),
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
        # trucks_here = trucks.filter(last_position__within=boundaries)
        # NOTE: we might want to verify that the provided commune is correct with regards to the position
        trucks_here = [tr for _, tr in trucks if tr['commune'] in com.name]
        commune_data = {
            'commune': com.name,
            'total': len(trucks_here),
            'cat_b': 0,
            'cat_c': 0
        }

        for th in trucks_here:
            truck_mam = int(th['mtm'])
            if truck_mam > 3500:
                commune_data['cat_c'] += 1
            else:
                commune_data['cat_b'] += 1

        result['cat_b'] += commune_data['cat_b']
        result['cat_c'] += commune_data['cat_c']
        result['table']['data'].append(commune_data)
    return result

####################
# AmCharts helpers #
####################


def build_chart_config(data, chart_type, xaxes, yaxes, series, legend=False):
    chart_dict = {
        'data': data,
        'xAxes': xaxes,
        'yAxes': yaxes,
        'series': series,
        'type': chart_type
    }

    if legend:
        # If legend is True, the default legend is enabled.
        if isinstance(legend, bool):
            chart_dict['legend'] = {
                'type': "Legend"
            }
        # Alternatively, one can provide a custom dict config for their legend
        else:
            chart_dict['legend'] = legend

    return chart_dict


def make_category_value_axes(category, xlabel=None, ylabel=None):
    x_axis = {
        'type': 'CategoryAxis',
        'dataFields': {
            'category': category
        }
    }

    if xlabel is not None:
        x_axis['title'] = {'text': xlabel}

    y_axis = {
        'type': 'ValueAxis'
    }

    if ylabel is not None:
        y_axis['title'] = {
            'text': ylabel
        }

    return x_axis, y_axis


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

    x_axis, y_axis = make_category_value_axes(category, xlabel, ylabel)

    columns = {
        'tooltipText': '{categoryX}: {valueY}'
        # Note: further customization of table should happen client-side
    }

    series = make_category_series(
        'ColumnSeries', category, value, name, columns)

    chart_dict = build_chart_config(
        data, 'XYChart', [x_axis], [y_axis], [series])

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
            'opposite': True  # To display values on top of the chart instead of bottom
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
            'name': val.replace('_', ' '),
            'columns': {
                'template': {
                    'tooltipText': "{name}: {valueX}",
                    'height': "90%"
                }
            }
        }

        series.append(ser)

    chart_dict = build_chart_config(data, 'XYChart', [x_axis], [
                                    y_axis], series, legend=True)

    return chart_dict


def boxplot_line(category, value, start, end):
    return {
        'type': 'StepLineSeries',
        'dataFields': {
                'categoryX': category,
                'valueY': value
        },
        'noRisers': True,
        'startLocation': start,
        'endLocation': end,
        'strokeWidth': 2,
        'stroke': 'black'
    }


def box_plot(data, category, xlabel=None, ylabel=None):

    # Based on this demo: https://www.amcharts.com/demos/box-plot-chart/
    # This is actually a candlestick chart, but the box limits are those of a boxplot

    x_axis, y_axis = make_category_value_axes(category, xlabel, ylabel)

    series = [
        {
            # Candlestick series to draw the box
            'type': 'CandlestickSeries',
            'dataFields': {
                'categoryX': category,
                'lowValueY': 'min',
                'valueY': 'Q1',
                'openValueY': 'Q3',
                'highValueY': 'max'
            },
            'columns': {
                'column': {
                    'tooltipText': 'Min:{min}\nQ1:{Q1}\nMedian:{median}\nQ3:{Q3}\nMax:{max}',
                    # Color customization
                    'fill': 'rgba(0, 0, 0, 0.2)',
                    'stroke': 'black',
                }
            },

            # Customization for boxplot (drop some candlestick functionality)
            'simplifiedProcessing': True,
            'riseFromOpenState': None,
            'dropFromOpenState': None,



        },
        # Median line
        boxplot_line(category, 'median', 0.1, 0.9),
        # Top line
        boxplot_line(category, 'max', 0.2, 0.8),
        # Top line
        boxplot_line(category, 'min', 0.2, 0.8)
    ]

    chart_dict = build_chart_config(
        data, 'XYChart', [x_axis], [y_axis], series)

    return chart_dict


###################
# Concrete charts #
###################


def category_distribution(trucks, communes, sort_key='cat_c'):
    """
    Generates a configuration for a chart that shows the distribution of trucks over communes and over categories in a clustered bar chart.

    :param trucks: Previously retrieved queryset of trucks.
    :type trucks: ~django.db.models.query.QuerySet
    :param communes: Queryset of Brussels communes.
    :type communes: ~django.db.models.query.QuerySet
    :param sort_key: key to use for ordering the bars in a commune (i.e. which to show first), defaults to 'cat_c'
    :type sort_key: str, optional
    :return: Configuration for instantiating the chart on the client.
    :rtype: dict
    """

    data = []

    for com in communes:
        boundaries = com.boundaries
        # NOTE: IMPORTANT! As a placeholder we use the truck's last position. For the real deal this should use RT data or the position at a certain time
        # trucks_here = trucks.filter(last_position__within=boundaries) #TODO: modify this to use the RT data
        trucks_here = []
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

    data.sort(key=lambda com: com[sort_key])  # Sort the list on the given key
    return clustered_bar_chart(data, 'commune', ['cat_b', 'cat_c'])


def time_of_day_distribution(truck_counts: list):
    """
    Constructs a configuration for a barchart that displays the number of trucks 
    for each time-foday. Can be used for streets or communes interachangeably, as only 
    a list of 24 truck counts is required.

    :param truck_counts: List of number of trucks (average, max, min, etc.) for every time-of-day [0-24)
    :type truck_counts: list
    :return: Barchart configuration for Amcharts
    :rtype: dict
    """
    # TODO: test with real data, might need formatter

    cat = 'time_of_day'
    val = 'truck_total'

    data_list = []

    # 24 hours in a day
    for i in range(24):
        data_list.append({
            cat: i,
            val: truck_counts[i]
        })

    return bar_chart(data_list, 'Truck activity', cat, val)


def delay_distribution(delays, resolution='time_of_day'):

    time_intervals = get_time_intervals(resolution)

    columndata_list = []

    # Compute normal distribution of delays if no batch intervals to fit
    # NOTE: we assume delays are normally distibuted, we might want to investigate this. This figure can give an indication if it fits
    # TODO: review how to do a histogram with amcharts
    # if batch_intervals is None:
    #     # Fit a normal distribution to the data:
    #     mu, std = norm.fit(delays)

    #     xmin = min(delays)
    #     xmax = max(delays)

    #     x = np.linspace(xmin, xmax, 25)
    #     p = norm.pdf(x, mu, std)

    #     delay_hist, bin_edges = np.histogram(delays, bins=25, density=True)

    #     linedata_list = []

    #     for i, delay_freq in enumerate(delay_hist):
    #         bin_center = (bin_edges[i] + bin_edges[i+1]) / 2
    #         columndata_list.append({
    #             'bin': bin_center,
    #             'freq': delay_freq
    #         })

    for i, delay in enumerate(delays):
        columndata_list.append(
            {
                'delay': delay,
                'batch_interval': time_intervals[i]
            }
        )

    return bar_chart(columndata_list, 'Typical Delay', 'batch_interval', 'delay', 'Hour-of-the-Day', 'Delay')
