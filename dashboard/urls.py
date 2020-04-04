from django.urls import path
from .views import (
    DashboardHomeView,
    DashboardView,
    LineChartView
)
from . import views

urlpatterns = [
    path('dashboard/', DashboardHomeView.as_view(), name='dashboard-home'),
    path('dashboard/<slug:userHash>/', DashboardView.as_view(), name='dashboard-details'),
    path('line-chart/', LineChartView.as_view(), name='line-chart'),
]
