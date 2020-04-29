from datetime import datetime
import shutil
import logging
import os
import time
import json
import uuid
import zipfile

from celery import shared_task
from django.shortcuts import get_object_or_404
from django_celery_results.models import TaskResult
from niota import verify
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from applications.archives.models import Archive
from applications.archives.models import Records
from applications.archives.serializer import ParserTaskSerializer
from applications.archives.serializer import ArchiveSerializer
#from applications.archives.serializer import ArchiveAnalysisSerializer
#from applications.data_owners.models import DataOwner
#from applications.data_owners.serializer import DataOwnerSerializer
#from bitsocial_tasks.tasks import parse_archive


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
verify_obj = verify.NumbersVerify(logger)


class ArchiveViewset(viewsets.ModelViewSet):
    serializer_class = ArchiveSerializer

    def get_queryset(self):
        return Archive.objects.all()

    def create_tmp_dir(self, public_key, file_obj):
        dir_prefix = '/tmp'
        dir_suffix = public_key
        dir_path = os.path.join(dir_prefix, dir_suffix)
        zipfile = os.path.join(dir_path, file_obj.name)
        if not os.path.exists(dir_path):
            try:
                original_umask = os.umask(0)
                os.makedirs(dir_path, 0o777)
            finally:
                os.umask(original_umask)
        with open(zipfile, 'wb+') as dst:
            logger.debug(type(file_obj))
            logger.debug(file_obj.name)
            logger.debug(file_obj.size)
            if file_obj.multiple_chunks():
                for chunk in file_obj.chunks():
                    dst.write(chunk)
            else:
                dst.write(file_obj.read())
        return dir_path, file_obj.name

    def get_id_offset(self):
        return int(round(time.time()*1000))*1000000

    def create(self, request):
        serializer = ArchiveSerializer(data=request.data)
        #public_key = request.data['data_owner']
        file_obj = request.data['file']
        tmp_dir, file_name = self.create_tmp_dir(
            'fake_public_key', file_obj
        )

        if serializer.is_valid():
            serializer.save()
            #archive_id = serializer.data['id']
            #public_key = serializer.data['data_owner']
            file_obj = request.data['file']
            #t = parse_archive.delay(
            #    tmp_dir,
            #    file_name,
            #    public_key,
            #    request.META.get('HTTP_AUTHORIZATION').split(' ')[1],
            #    self.get_id_offset(),
            #)

            #t = parse_archive.delay()
            #for attempt in range(5):
            #    print('Attempt #{}'.format(attempt + 1))
            #    try:
            #        task = TaskResult.objects.get(task_id=t.task_id)
            #    except TaskResult.DoesNotExist:
            #        time.sleep(0.1)
            #        print('TaskResult does not exist yet ({}/5)'.format(attempt + 1))
            #        continue
            #    break
            #task_serializer = ParserTaskSerializer(task)
            #return Response(task_serializer.data, status.HTTP_201_CREATED)
            filepath = os.path.join(tmp_dir, file_name)
            target_dirpath = unzip(filepath, tmp_dir)
            update_records_table(target_dirpath)
            clean(filepath, target_dirpath)
            identity = os.path.basename(target_dirpath)
            access_url = create_access_url(identity)
            return Response(access_url, status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status.HTTP_400_BAD_REQUEST)


def unzip(filepath, root_dirpath, target_dirname=''):
    """Unzip file to root_dirpath/target_dirname/

    Target_dirname is a random UUID by default, and user can specify it.
    """
    if target_dirname == '':
        target_dirname = str(uuid.uuid4())
    target_dirpath = os.path.join(root_dirpath, target_dirname)
    print(f'FilePath: {filepath}')
    print(f'TargetDir: {target_dirpath}')
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(target_dirpath)
    return target_dirpath


def transaction_mapping(verification_filepath):
    with open(verification_filepath) as f:
        return json.load(f)


def update_records_table(target_dirpath):
    """Read records in target dir and add into database.
    """
    json_filepaths = [os.path.join(target_dirpath, filename)
                      for filename in os.listdir(target_dirpath)]
    identity = os.path.basename(target_dirpath)
    mapping = transaction_mapping(
                  os.path.join(target_dirpath,
                               'verification.json'))
    print(f'JSON files: {json_filepaths}')
    print('Identity: ' + identity)
    print(f'Mapping: {mapping}')
    for filepath in json_filepaths:
        filename = os.path.basename(filepath)

        # Skip the verification file because it does not contain a record,
        # but contains the ledger transaction mapping.
        if filename == 'verification.json':
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = json.load(f)
            print('bundlehash: {}'.format(mapping[filename]))
            try:
                verification = verify_obj.verify(mapping[filename], content)
            except Exception as e:
                print(e)
                print('Failed bundlehash: {}'.format(mapping[filename]))
                verification = False
            print('verification: {}'.format(verification))
            r = Records(identity = identity,
                        timestamp = unix_time_timestamp(content['timestamp']),
                        content = content,
                        verification = verification)
            r.save()
    print(f'Records: {Records.objects.all()}')


def clean(filepath, target_dirpath):
    print(f'Delete {filepath}')
    print(f'Delete {target_dirpath}')
    os.remove(filepath)
    shutil.rmtree(target_dirpath)


def create_access_url(unique_id):
    print(f'Use unique ID {unique_id} to get records from database')
    access_url = f'https://mylog14.numbersprotocol.io/dashboard/{unique_id}'
    return access_url


@shared_task(track_started=True)
def parse_archive():
    logger.info('Start unzipping temp zip')
#def parse_archive(tmp_dir, file_name, public_key, api_key, offset):
    #logger.info('Start unzipping temp zip')
    #unzip_temp_zip(file_name, tmp_dir)
    #remove_macosx_dir(tmp_dir)
    #logger.info('Start sending files to S3')
    #directory_to_s3(public_key, tmp_dir)

    #tmp_json_dir = '{}-json'.format(tmp_dir)
    #if not os.path.exists(tmp_json_dir):
    #    os.makedirs(tmp_json_dir, 0o777)

    #logger.info('Start parsing and posting')
    #parser = Parser(tmp_dir, tmp_json_dir, public_key, api_key, offset)
    #parser.parse()

    #check_data_parsed(tmp_dir, tmp_json_dir, 'posts', 'posts')
    #check_data_parsed(tmp_dir, tmp_json_dir, 'likes_and_reactions', 'reactions')

    #remove_temp_dir(tmp_dir)
    #remove_temp_dir(tmp_json_dir)
    #logger.info('Data upload completed')

    #sentiment_analyzer = SentimentAnalyzer(public_key)
    #sentiment_analyzer.analyze()
    #logger.info('Sentiment analysis completed')


def unix_time_timestamp(t):
    """Convert millisec and microsec timestamps to Unix time timestamp.

    App (Javascript) uses 13-digit timestamp (msecs),
    so we convert it to 10-digit Unix time timestamp (secs) for Python.
    """
    timestamp = int(t)
    digits = len(str(timestamp))
    if digits == 10:
        return timestamp
    elif digits == 13:
        return int(timestamp / 1000)
    elif digits == 16:
        return int(timestamp / 1000000)
    else:
        logger.warn((
            'Timestamp {0} has unknown digits {1},'
            ' use the timestamp without any guarantee'.format(t, digits)
        ))
        return timestamp