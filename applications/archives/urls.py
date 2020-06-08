from django.urls import path
from .views import ReviewHomeView, DashboardHomeView, DataView

urlpatterns = [
    path('', ReviewHomeView.as_view(), name='dashboard-home'),
    path('<slug:userHash>/', DashboardHomeView.as_view(), name='dashboard-details'),
    path('/line-chart/<slug:userHash>/', DataView.as_view(), name='line-chart'),
    path('/location-mapping/', DataView.as_view(), name='location-mapping')
]