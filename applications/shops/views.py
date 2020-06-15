from django.shortcuts import render
from rest_framework import viewsets

from applications.shops.models import Shop
from applications.shops.serializers import ShopSerializer


class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()