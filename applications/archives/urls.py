from django.urls import path
from .views import (
    ReviewHomeView,
    DashboardHomeView
)
from . import views

urlpatterns = [
    path('', ReviewHomeView.as_view(), name='dashboard-home'),
    path('<slug:userHash>/', DashboardHomeView.as_view(), name='dashboard-details'),
    path('line-chart/', views.line_chart, name='line-chart')
]