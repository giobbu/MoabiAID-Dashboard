import os

import matplotlib.pyplot as plt
import numpy as np

import django.forms as forms
from django.template.loader import render_to_string

from mobiaid.settings import MEDIA_ROOT

from dashboard.data.figures import box_plot, delay_distribution


def compute_delay_stats(delays, time_frame):
    # Current timeframe will be a vector, while others will be a 2D matrix where we want min and max for each row
    if time_frame != 'current':
        np_axis = 1
        # For matrix input, we also compute the statistics over all values
        stats = {
            'tot_delay_min': np.amin(delays),
            'tot_delay_max': np.amax(delays),
            'tot_delay_mean': np.mean(delays),
            'tot_delay_std': np.std(delays),
            'tot_delay_percentiles': np.percentile(delays, [25, 50, 75])
        }
    else:
        np_axis = None
        stats = {}

    stats.update({
        'batch_delay_min': np.amin(delays, axis=np_axis),
        'batch_delay_max': np.amax(delays, axis=np_axis),
        'batch_delay_mean': np.mean(delays, axis=np_axis),
        'batch_delay_std': np.std(delays, axis=np_axis),
        'batch_delay_percentiles': np.percentile(delays, [25, 50, 75], axis=np_axis)
    })

    return stats

# NOTE: Same as in notebook with matplotlib. Try to make this with amcharts for interactive, but this is a good backup
#       Other alternative: mpld3 to create D3.js figures from matplotlib figures


def plot_delay_messages(delay_list, minime, maxime, delay_min, delay_mean, delay_max, delay_std, retrieve_hour, retrieve_date):

    day = maxime // (24 * 3600)
    maxime = maxime % (24 * 3600)
    hour = maxime // 3600
    maxime %= 3600
    minutes = maxime // 60
    maxime %= 60
    seconds = maxime
    print("Max Delay: %d day,  %d hour, %d minutes, %d seconds" %
          (day, hour, minutes, seconds))
    print('')

    Minutes_delay = [i for i in delay]
    Minutes_max = [i for i in delay_max]
    Minutes_mean = [i for i in delay_mean]
    Minutes_min = [i for i in delay_min]

    plt.bar(retrieve_hour, Minutes_max, align='center', alpha=0.5)
    plt.ylabel('OBU Delay (Minutes)')
    plt.xlabel('Batch Interval (Hours)')
    plt.title('Delay per Batch Interval')
    # plt.show()
    plt.savefig(os.path.join(MEDIA_ROOT, 'figures/batch_delay.svg'))

    tot_mean = np.mean(delay_mean)

    plt.plot(retrieve_date, Minutes_mean)
    plt.bar(retrieve_date, delay_std, color='r', alpha=0.2)
    plt.axhline(tot_mean, color='g', linestyle='--')
    # plt.show()
    plt.savefig(os.path.join(MEDIA_ROOT, 'figures/mean_deviation_delay.svg'))

    last = 15

    if len(retrieve_date) >= last:
        retrieve_date = retrieve_date[-last:]
        Minutes_max = Minutes_max[-last:]
        Minutes_mean = Minutes_mean[-last:]
        Minutes_min = Minutes_min[-last:]
        delay_std = delay_std[-last:]
        delay_list = delay_list[-last:]

    plt.scatter(retrieve_date, Minutes_max, color='r')
    plt.plot(retrieve_date, Minutes_mean)
    plt.scatter(retrieve_date, Minutes_min)
    plt.bar(retrieve_date, delay_std, color='r', alpha=0.2)
    plt.axhline(tot_mean, color='g', linestyle='--')
    # plt.show()
    plt.savefig(os.path.join(MEDIA_ROOT, 'figures/mean_delay.svg'))

    plt.boxplot(delay_list)
    # plt.show()
    plt.savefig(os.path.join(MEDIA_ROOT, 'figures/delay_boxplot.svg'))

class TimeFrameSelect(forms.Form):
    select_timeframe = forms.ChoiceField(choices=[('CU', 'Current batch'), ('DAY', 'Daily'), ('WEEK', 'Weekly'), ('ALL', 'All time')])


def delay_analysis(delays, time_frame):

    delay_stats = compute_delay_stats(delays, time_frame)

    fig_configs = {} 
    table_configs = {}

    map_data = {} # TODO: read/generate the geojson for map display

    # TODO: build appropriate chart and table configurations 
    if time_frame == 'current':
        fig_configs['boxplot'] = box_plot([{
            'batch': 'Latest Batch',
            'min': delay_stats['batch_delay_min'],
            'max': delay_stats['batch_delay_max'],
            'Q1': delay_stats['batch_delay_percentiles'][0],
            'median': delay_stats['batch_delay_percentiles'][1],
            'Q3': delay_stats['batch_delay_percentiles'][2],
        }], 'batch')

    ctx = {
        'timeframe': time_frame,
        'figure_configs': fig_configs,
        'table_configs': table_configs,
        'map_data': map_data,
        'analytics_controls': TimeFrameSelect()
    }  

    return render_to_string('dashboard/dashboard_tabs/delay_analysis.html', context=ctx)
