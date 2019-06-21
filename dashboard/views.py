from django.shortcuts import render

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
