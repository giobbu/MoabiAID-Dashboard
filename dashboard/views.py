from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .data.request_handlers import *
from .utils import MapControls, get_analytic_controls

def home(request):
    """
    Home page view. Simply renders the index template and returns the HTMl page.
    
    :param request: The incoming HTTP request to the home URL.
    :type request: ~django.http.HttpRequest
    :return: The rendered index page.
    :rtype: ~django.http.HttpResponse
    """
    context = {'nbar': 'home'} # Manages nav-bar from here instead of JS
    return render(request, 'dashboard/index.html', context=context)

def dashboard(request):
    """
    View for the Dashborad page. Includes some basic map controls for the real time tab. 
    Content for other tabs is handleded by the *load_dashboard_tab* view.
    
    :param request: The incoming HTTP request to the dashboard URL.
    :type request: ~django.http.HttpRequest
    :return: Dashboard page with navigation and tab elements. Tab content is laoded with Javascript.
    :rtype: ~django.http.HttpResponse
    """
    context = {
        'nbar': 'dashboard',
        'map_controls': MapControls()
        } 
    return render(request, 'dashboard/dashboard.html', context=context)

# def charts(request):
#     context = {'nbar': 'charts'} # Manages nav-bar from here instead of JS
#     return render(request, 'dashboard/charts.html', context=context)

def about(request):
    """
    View for the About page. This page consists mostly of static HTML content
    
    :param request: The incoming HTTP request to the about URL.
    :type request: ~django.http.HttpRequest
    :return: Rendered template for the About page.
    :rtype: ~django.http.HttpResponse
    """
    context = {'nbar': 'about'}
    return render(request, 'dashboard/about.html', context=context)

def data(request):
    """
    View that handles ajax data requests for tables, dynamic figures and any type of requests that need to access the database.
    Only works with GET requests.
    
    :param request: A GET request with the following parameters: 'table' specifies the name of the table to load for table requests. 
                    'data' specifies the type of data to load. 'data_usage' specifies what the data would be used for (not for table requests).
    :type request: ~django.http.HttpRequest
    :return: JSON serialized data for client-side processing.
    :rtype: ~django.http.HttpResponse or ~django.http.JsonResponse
    """
    print('Processing data request')
    table = request.GET.get('table')
    req_data = request.GET.get('data')

    usage = request.GET.get('data_usage')

    result_data = get_data(table, req_data, usage)
    print('Request processed')
    if isinstance(result_data, str):
        response = HttpResponse(result_data, content_type='text/json') # Data already serialized
    else:
        response = JsonResponse({'data': result_data})
    # print(response.content)
    return response

def analysis(request, analysis):
    time_frame = request.GET.get('timeFrame')

    response_html = get_analysis_template(analysis, **request.GET.dict())

    return HttpResponse(response_html)

def load_dashboard_tab(request):
    """
    View that renders the HTML for specified dashboard tab, to be included in the tab element of the Dashboard page.
    Only works with GET requests.

    NOTE: Implement content rendering for additional tabs here!
    
    :param request: HTTP GET request object with a 'tab' parameter that specifies the tab to load.
                    The 'content' parameter is used to determine which data the user selected, currently only for loading appropriate control elements.
    :type request: ~django.http.HttpRequest
    :return: Rendered HTML template for the requested tab.
    :rtype: ~django.http.HttpResponse
    """
    tab = request.GET.get('tab')
    selected_content = request.GET.get('content')

    if tab == 'analytics':
        template = 'dashboard/dashboard_tabs/analytics.html'
        ctx = {
                'analytics_controls': get_analytic_controls(selected_content)
            }
    
    return render(request, template, context=ctx)
            

    


