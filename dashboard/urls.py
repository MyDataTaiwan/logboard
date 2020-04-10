from django.urls import path
from .views import (
    DashboardHomeView,
    DashboardDetailView
)
from . import views

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard-home'),
    path('<slug:userHash>/', DashboardDetailView.as_view(), name='dashboard-details'),
    path('line-chart/', views.line_chart, name='line-chart')
]