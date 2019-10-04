from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .data.request_handlers import *
from .utils import MapControls

# Create your views here.
def home(request):
    context = {'nbar': 'home'} # Manages nav-bar from here instead of JS
    return render(request, 'dashboard/index.html', context=context)

def dashboard(request):
    context = {
        'nbar': 'dashboard',
        'map_controls': MapControls()
        } 
    return render(request, 'dashboard/dashboard.html', context=context)

# def charts(request):
#     context = {'nbar': 'charts'} # Manages nav-bar from here instead of JS
#     return render(request, 'dashboard/charts.html', context=context)

def about(request):
    context = {'nbar': 'about'}
    return render(request, 'dashboard/about.html', context=context)

def data(request):
    table = request.GET.get('table')
    req_data = request.GET.get('data')

    usage = request.GET.get('data_usage')

    result_data = get_data(table, req_data, usage)
    if isinstance(result_data, str):
        response = HttpResponse(result_data, content_type='text/json') # Data already serialized
    else:
        response = JsonResponse({'data': result_data})
    # print(response.content)
    return response

    


