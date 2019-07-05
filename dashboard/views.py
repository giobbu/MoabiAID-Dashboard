from django.shortcuts import render
from django.http import JsonResponse

from .data.request_handlers import *

# Create your views here.
def home(request):
    context = {'nbar': 'home'} # Manages nav-bar from here instead of JS
    return render(request, 'dashboard/index.html', context=context)

def dashboard(request):
    context = {'nbar': 'dashboard'} # Manages nav-bar from here instead of JS
    return render(request, 'dashboard/dashboard.html', context=context)

def charts(request):
    context = {'nbar': 'charts'} # Manages nav-bar from here instead of JS
    return render(request, 'dashboard/charts.html', context=context)

def data(request):
    table = request.GET.get('table')
    req_data = request.GET.get('data')

    result_data = { # Wrap in dict as some data requests might return a list
        'data': get_data(table, req_data)
        }

    return JsonResponse(result_data)

    


