from django.test import TestCase

from apps.records.models import Record
from apps.users.models import CustomUser


class RecordTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user('logboard-user', 'user@logboard.io', 'simplepassword')
        Record.objects.create(transaction_hash='1234567890', owner=user)

    def test_str_return_transaction_hash(self):
        """call str() on Record instance returns transaction_hash"""
        record = Record.objects.get(transaction_hash='1234567890')
        self.assertEqual(str(record), '1234567890')
