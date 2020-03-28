from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard-home'),
    path('population-chart/', views.population_chart, name='population-chart'),
    path('test/', views.test, name='dashboard-test'),
]
