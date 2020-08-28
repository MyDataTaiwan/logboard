from datetime import datetime, time, timedelta
import json
import logging
import pytz

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.records.filters import RecordFilter
from apps.records.models import Record
from apps.records.serializers import RecordSerializer, RecordCreateSerializer, TemplateSerializer
from apps.records.tasks import parse_record
from apps.users.models import CustomUser
from utils.data_template import DataTemplate


logger = logging.getLogger(__name__)


def simplify_records(records: list, template_name: str):
    template = DataTemplate(template_name)
    for record in records:
        record.pop('proof')
        record['vital_signs'] = {}
        record['symptoms'] = {}
        for field in record['fields']:
            name = field['name']
            value = field['value']
            data_group = template.get_field_attr(name, 'dataGroup')
            if not data_group:
                data_group = field.get('dataGroup', None)
            if data_group == 'vitalSigns':
                record['vital_signs'][name] = value
            elif data_group == 'symptoms' or data_group == 'checklist':
                record['symptoms'][name] = value
        record.pop('fields')
    return records


def parse_to_summary(records: list, template_name: str):
    def update(arr, val, append, accumulate=False):
        if append:
            arr.append(val)
        else:
            if val is None:
                pass
            elif (isinstance(arr[-1], bool)):
                arr[-1] = arr[-1] or val
            elif (isinstance(arr[-1], (int, float))):
                if accumulate:
                    arr[-1] += val
                else:
                    arr[-1] = max(arr[-1], val)
            else:
                arr[-1] = val
        return arr

    records = simplify_records(records, template_name)
    res = {
        'id_list': [],
        'date': [],
        'vital_signs': {},
        'symptoms': [],
        'photo_list': [],
        'thumbnail_list': [],
    }
    for record in records:
        timestamp_datetime = datetime.strptime(record['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        date = timestamp_datetime.astimezone(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d')
        append = (date not in res['date'])
        update(res['date'], date, append)
        if append:
            res['id_list'].append([record['id']])
            res['photo_list'].append([record['photo']])
            res['thumbnail_list'].append([record['thumbnail']])
        else:
            res['id_list'][-1].append(record['id'])
            res['photo_list'][-1].append(record['photo'])
            res['thumbnail_list'][-1].append([record['thumbnail']])
        for key, val in record['vital_signs'].items():
            if not res['vital_signs'].get(key, None):
                res['vital_signs'][key] = []
            accumulate = (key == 'urineVolume')
            update(res['vital_signs'][key], val, append, accumulate)
        for key, val in record['symptoms'].items():
            symptom = next((x for x in res['symptoms'] if x['name'] == key), None)
            if not symptom:
                symptom = {
                    'name': key,
                    'symptom': [],
                }
                res['symptoms'].append(symptom)
            update(symptom['symptom'], val, append)

    return res


def parse_to_today(records: list, template_name: str):
    records = simplify_records(records, template_name)
    res = {
        'id': [],
        'timestamp': [],
        'vital_signs': {},
        'symptoms': [],
        'photos': [],
        'thumbnails': [],
    }
    for record in records:
        res['id'].append(record['id'])
        timestamp_datetime = datetime.strptime(record['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        timestamp = timestamp_datetime.astimezone(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')
        res['timestamp'].append(timestamp),
        for key, val in record['vital_signs'].items():
            if not res['vital_signs'].get(key, None):
                res['vital_signs'][key] = []
            res['vital_signs'][key].append(val)
        for key, val in record['symptoms'].items():
            symptom = next((x for x in res['symptoms'] if x['name'] == key), None)
            if not symptom:
                symptom = {
                    'name': key,
                    'symptom': [],
                }
                res['symptoms'].append(symptom)
            symptom['symptom'].append(val)
        res['photos'].append(record['photo'])
        res['thumbnails'].append(record['thumbnail'])
    return res


class RecordViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = RecordSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecordFilter

    def get_queryset(self):
        user = self.request.user
        return Record.objects.filter(owner=user).order_by('-id')

    def retrieve(self, request, pk=None):
        uid = request.query_params.get('uid', None)
        no_valid_id_error = {
            'error': 'Query param uid is required.',
        }
        if not uid:
            return Response(no_valid_id_error, status=status.HTTP_400_BAD_REQUEST)
        try:
            CustomUser.objects.get(pk=uid)
        except ObjectDoesNotExist:
            error = {'error': 'User ID not found.'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        records = Record.objects.filter(owner__id=uid).get(id=pk)
        serializer = RecordSerializer(records)
        return Response(serializer.data, status.HTTP_200_OK)

    def list(self, request):
        id = request.query_params.get('uid', None)
        no_valid_id_error = {
            'error': 'Query param uid is required.',
        }
        if not id:
            return Response(no_valid_id_error, status=status.HTTP_400_BAD_REQUEST)
        cache_key = 'record_list_{}'.format(id)
        data = cache.get(cache_key)
        if data:
            return Response(data, status.HTTP_200_OK)
        try:
            CustomUser.objects.get(pk=id)
        except ObjectDoesNotExist:
            error = {'error': 'User ID not found.'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        records = Record.objects.filter(owner__id=id).order_by('timestamp')
        serializer = RecordSerializer(records, many=True)
        cache.set(cache_key, serializer.data)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_anonymous:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        cache_key = 'record_list_{}'.format(request.user.id)
        serializer = RecordCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            transaction.on_commit(lambda: parse_record.delay(serializer.data['id']))
            cache.delete(cache_key)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def summary(self, request):
        def parse_date(date):
            return datetime.strptime(date, '%Y-%m-%d') - timedelta(hours=8)
        id = request.query_params.get('uid', None)
        if not id:
            return Response(
                {'error': ' uid must be specified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date must be specified'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        template = request.query_params.get('template', None)
        if not template:
            return Response(
                {'error': 'template must be specified'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            CustomUser.objects.get(pk=id)
        except ObjectDoesNotExist:
            error = {'error': 'User ID not found.'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        try:
            date_range = (
                parse_date(start_date),
                parse_date(end_date) + timedelta(days=1),
            )
        except ValueError:
            return Response(
                {
                    'error': 'Either date format {} or {} is incorrect. Should be YYYY-MM-DD'.format(
                        start_date, end_date
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        records = Record.objects.filter(
            owner__id=id, template_name__exact=template, timestamp__range=date_range
        ).order_by('timestamp')
        serializer = RecordSerializer(records, many=True)
        res = parse_to_summary(serializer.data, template)
        return Response(res, status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def today(self, request):
        def get_today():
            now = datetime.now(pytz.timezone('Asia/Taipei'))
            return datetime.combine(now.date(), time()) - timedelta(hours=8)
        id = request.query_params.get('uid', None)
        if not id:
            return Response(
                {'error': ' uid must be specified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        template = request.query_params.get('template', None)
        if not template:
            return Response(
                {'error': 'template must be specified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            CustomUser.objects.get(pk=id)
        except ObjectDoesNotExist:
            error = {'error': 'User ID not found.'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        date_range = (get_today(), get_today() + timedelta(days=1))
        records = Record.objects.filter(
            owner__id=id, template_name__exact=template, timestamp__range=date_range
        ).order_by('timestamp')
        serializer = RecordSerializer(records, many=True)
        res = parse_to_today(serializer.data, template)
        return Response(res, status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='past-days')
    def past_days(self, request):
        def get_today():
            now = datetime.now(pytz.timezone('Asia/Taipei'))
            return datetime.combine(now.date(), time()) - timedelta(hours=8)
        range_type = request.query_params.get('range', None)
        if not range_type:
            return Response(
                {'error': ' range must be specified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if range_type not in ['this-week', 'two-weeks', 'this-month']:
            return Response(
                {'error': ' invalid range'},
                status=status.HTTP_400_BAD_REQUEST
            )
        id = request.query_params.get('uid', None)
        if not id:
            return Response(
                {'error': ' uid must be specified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        template = request.query_params.get('template', None)
        if not template:
            return Response(
                {'error': 'template must be specified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            CustomUser.objects.get(pk=id)
        except ObjectDoesNotExist:
            error = {'error': 'User ID not found.'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        if range_type == 'this-week':
            start_date = get_today() - timedelta(days=7)
        elif range_type == 'two-weeks':
            start_date = get_today() - timedelta(days=14)
        elif range_type == 'this-month':
            start_date = get_today() - timedelta(days=30)
        end_date = get_today() + timedelta(days=1)
        date_range = (start_date, end_date)
        records = Record.objects.filter(
            owner__id=id, template_name__exact=template, timestamp__range=date_range
        ).order_by('timestamp')
        serializer = RecordSerializer(records, many=True)
        res = parse_to_summary(serializer.data, template)
        return Response(res, status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='templates')
    def templates(self, request):
        template = request.query_params.get('template')
        cache_key = 'template_{}'.format(template)
        data = cache.get(cache_key)
        if data:
            return Response(data, status.HTTP_200_OK)
        serializer = TemplateSerializer(data={'template': template})
        if serializer.is_valid():
            cache.set(cache_key, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)