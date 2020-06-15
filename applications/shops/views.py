from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from applications.shops.models import Shop
from applications.shops.serializers import ShopSerializer, ShopDetailSerializer


class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = ShopDetailSerializer(instance)
        return Response(serializer.data)