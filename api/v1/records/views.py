from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from api.v1.records.models import Record
from api.v1.records.serializer import RecordSerializer


# ViewSets define the view behavior.
class RecordViewSet(viewsets.ModelViewSet):
    #queryset = Record.objects.all()
    #queryset = ''
    #serializer_class = RecordSerializer

    #def get_queryset(self):
    #    groups = self.request.user.groups.all()
    #    return Record.objects.filter(
    #        data_owner__authorized_services__in=groups,
    #    ).distinct().order_by('-uploaded_at')

    def create(self, request):
        serializer = RecordSerializer(data=request.data)
        #public_key = request.data['data_owner']
        #file_obj = request.data['file']
        #tmp_dir, file_name = self.create_tmp_dir(
        #    public_key, file_obj
        #)

        print('data: {}'.format(request.data))

        if serializer.is_valid():
            serializer.save()
            #archive_id = serializer.data['id']
            #public_key = serializer.data['data_owner']
            #file_obj = request.data['file']
            #t = parse_archive.delay(
            #    tmp_dir,
            #    file_name,
            #    public_key,
            #    request.META.get('HTTP_AUTHORIZATION').split(' ')[1],
            #    self.get_id_offset(),
            #)
            #for attempt in range(5):
            #    try:
            #        task = TaskResult.objects.get(task_id=t.task_id)
            #    except TaskResult.DoesNotExist:
            #        time.sleep(0.1)
            #        continue
            #    break
            #task_serializer = ParserTaskSerializer(task)
            #return Response(task_serializer.data, status.HTTP_201_CREATED)
            print('Receive records POST')
            return Response('get post', status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)
