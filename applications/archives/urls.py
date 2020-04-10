from django.urls import path
from .views import ReviewHomeView, DashboardHomeView, LineChart, MapView

urlpatterns = [
    path('', ReviewHomeView.as_view(), name='dashboard-home'),
    path('<slug:userHash>/', DashboardHomeView.as_view(), name='dashboard-details'),
    path('/line-chart/', LineChart.as_view(), name='line-chart'),
    path('/location-mapping/', MapView.as_view(), name='location-mapping')
]