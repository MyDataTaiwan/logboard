from django.test import TestCase

from apps.users.models import CustomUser


class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create_user('logboard-user', 'user@logboard.io', 'simplepassword')

    def test_str_return_username(self):
        """call str() on Record instance returns transaction_hash"""
        user = CustomUser.objects.get(username='logboard-user')
        self.assertEqual(str(user), 'logboard-user')
