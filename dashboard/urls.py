from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # path("charts/", views.charts, name="charts"),
    path("data/", views.data, name="data"),
    path("about/", views.about, name="about"),
    path('select2/', include('django_select2.urls')),
    path('analysis/<analysis>/', views.analysis, name='analysis')
]
