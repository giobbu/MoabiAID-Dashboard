from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # path("charts/", views.charts, name="charts"),
    path("data/", views.data, name="data"),
    path("about/", views.about, name="about")
]
