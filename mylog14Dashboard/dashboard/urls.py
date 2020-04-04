from django.urls import path
from .views import (
    DashboardHomeView,
    DashboardView,
    LineChartView
)
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard-home'),
    path('details/', DashboardView.as_view(), name='dashboard-details'),
    path('line-chart/', LineChartView.as_view(), name='line-chart'),
]
