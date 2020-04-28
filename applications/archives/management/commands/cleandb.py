from datetime import datetime
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from applications.archives.models import Records


class Command(BaseCommand):
    help = 'Delete database items existing longer than 3 days'

    def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        ndays = 3
        datetime_ndays_ago = datetime.now() - timedelta(days=ndays)
        timestamp_ndays_ago = int(datetime_ndays_ago.timestamp())

        self.stdout.write(self.style.SUCCESS('{2} days ago: {0} ({1})'.format(datetime_ndays_ago, timestamp_ndays_ago, ndays)))

        self.stdout.write(self.style.SUCCESS('Delete old items'))
        Records.objects.filter(timestamp__lt=timestamp_ndays_ago).delete()

    def debug_list_all_timestamps(self):
        self.stdout.write(self.style.SUCCESS('all timestamps'))
        for obj in Records.objects.all().order_by('timestamp'):
            self.stdout.write(self.style.SUCCESS(obj.timestamp))

    def debug_list_ndays_ago_timestamps(self, ndays, timestamp_ndays_ago):
        self.stdout.write(self.style.SUCCESS('{} days ago timestamps'.format(ndays)))
        for obj in Records.objects.filter(timestamp__lt=timestamp_ndays_ago).order_by('timestamp'):
            self.stdout.write(self.style.SUCCESS(obj.timestamp))