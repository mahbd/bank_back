from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from main.models import ExternalBank

c = Client()
User = get_user_model()


class ExternalBankTest(TestCase):
    def setUp(self) -> None:
        self.api_url = reverse('external_bank-list')
        # create a user
        self.user = User.objects.create_user(username='test', password='test')
        self.user2 = User.objects.create_user(username='test2', password='test2')
        self.admin = User.objects.create_superuser(username='admin', password='admin')
        self.token = c.post(reverse('token_obtain_pair'), {'username': 'test', 'password': 'test'}).data['access']
        self.admin_token = c.post(reverse('token_obtain_pair'), {'username': 'admin', 'password': 'admin'}).data[
            'access']
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        self.admin_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.admin_token}', 'HTTP_Content-Type': 'application/json'}
        # create an external bank
        self.external_bank = ExternalBank()
        self.external_bank.user = self.user
        self.external_bank.name = 'test'
        self.external_bank.account_number = 'test'
        self.external_bank.information = 'test'
        self.external_bank.save()
        self.external_bank2 = ExternalBank()
        self.external_bank2.user = self.user2
        self.external_bank2.name = 'test2'
        self.external_bank2.account_number = 'test2'
        self.external_bank2.information = 'test2'
        self.external_bank2.save()

    def test_get_external_bank(self):
        response = c.get(self.api_url)
        self.assertEqual(response.status_code, 401)

    def test_get_external_bank_with_token(self):
        response = c.get(self.api_url, **self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.data['results']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[0]['user'], self.user.id)

    def test_get_external_bank_with_admin_token(self):
        response = c.get(self.api_url,
                         **{'HTTP_AUTHORIZATION': f'Bearer {self.admin_token}', 'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        data = response.data['results']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[1]['name'], 'test2')

    def test_create_external_bank(self):
        response = c.post(self.api_url, {'name': 'test2', 'account_number': 'test2', 'information': 'test2'},
                          **{'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 401)

    def test_create_external_bank_with_token(self):
        response = c.post(self.api_url, {'name': 'test2', 'account_number': 'test2', 'information': 'test2'},
                          **self.headers)
        self.assertEqual(response.status_code, 201, response.data)
        data = response.data
        self.assertEqual(data['name'], 'test2')
        self.assertEqual(data['user'], self.user.id)

    def test_update_external_bank(self):
        response = c.put(f'{self.api_url}{self.external_bank.id}/',
                         {'name': 'test2', 'account_number': 'test2', 'information': 'test2'},
                         **{'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 401)

    def test_update_external_bank_with_token(self):
        response = c.patch(f'{self.api_url}{self.external_bank.id}/',
                           {'name': 'test2', 'account_number': 'test2', 'information': 'test2'},
                           **self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['name'], 'test2')
        self.assertEqual(data['user'], self.user.id)

    def test_update_external_bank_of_another_user(self):
        response = c.patch(f'{self.api_url}{self.external_bank2.id}/',
                           {'name': 'test1', 'account_number': 'test2', 'information': 'test2'},
                           **self.headers)
        self.assertEqual(response.status_code, 404)

    def test_update_external_bank_of_another_user_with_admin_token(self):
        response = c.patch(f'{self.api_url}{self.external_bank.id}/', {'name': 'test2'},
                           **{'HTTP_AUTHORIZATION': f'Bearer {self.admin_token}'})
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['name'], 'test2')
        self.assertEqual(data['user'], self.user.id)
