import logging

from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.mylog.models import MyLog
from apps.mylog.serializers import MyLogSerializer


logger = logging.getLogger(__name__)


class MyLogViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MyLogSerializer

    def get_queryset(self):
        user = self.request.user
        return MyLog.objects.filter(owner=user)

    def create(self, request):
        serializer = MyLogSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
