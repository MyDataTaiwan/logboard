from django.urls import path
from .views import (
    DashboardHomeView,
    DashboardView
)
from . import views

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard-home'),
    path('dashboard/<slug:userHash>/', DashboardView.as_view(), name='dashboard-details'),
    path('line-chart/', views.line_chart, name='line-chart')
]