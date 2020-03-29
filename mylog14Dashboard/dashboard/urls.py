from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.home, name='dashboard-home'),
    path('population-chart/', views.population_chart, name='population-chart'),
]
