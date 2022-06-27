from random import choices, randint
from string import ascii_letters, digits

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import RequestsClient

from main.models import ExternalBank

c = RequestsClient()
User = get_user_model()

S_URL = 'http://testserver'


def create_external_bank(user: User, name: str = None, acc_num: str = None, info: str = None) -> ExternalBank:
    if not name:
        name = ''.join(choices(ascii_letters, k=randint(5, 10)))
    if not acc_num:
        acc_num = ''.join(choices(digits, k=randint(5, 10)))
    if not info:
        info = ''.join(choices(ascii_letters, k=randint(50, 100)))
    ex_bank = ExternalBank()
    ex_bank.user = user
    ex_bank.name = name
    ex_bank.account_number = acc_num
    ex_bank.information = info
    ex_bank.save()
    return ex_bank


def create_user(username: str = None, password: str = None, **kwargs) -> tuple[User, str]:
    if not username:
        username = ''.join(choices(ascii_letters, k=randint(5, 10)))
    if not password:
        password = ''.join(choices(ascii_letters, k=randint(5, 10)))
    user = User.objects.create_user(username=username, password=password, **kwargs)
    response = c.post(S_URL + reverse('token_obtain_pair'), {'username': username, 'password': password})
    token = response.json()['access']
    return user, token


def c_header(token: str = None, is_json: bool = True) -> dict:
    """
    Creates a header for a request
    """
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if is_json:
        headers['Content-Type'] = 'application/json'
    return headers


class ExternalBankTest(TestCase):
    def setUp(self) -> None:
        self.api_url = S_URL + reverse('external_bank-list')
        # create a user
        self.user, self.token = create_user()
        self.user2, self.token2 = create_user("test2", "test2")
        self.admin, self.admin_token = create_user("admin", "admin", is_superuser=True, is_staff=True)
        self.external_bank = create_external_bank(self.user, name='test')
        self.external_bank2 = create_external_bank(self.user2, name='test2')

    def test_get_external_bank(self):
        response = c.get(self.api_url)
        self.assertEqual(response.status_code, 401)

    def test_get_external_bank_with_token(self):
        response = c.get(self.api_url, headers=c_header(self.token))
        self.assertEqual(response.status_code, 200)
        data = response.json()['results']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[0]['user'], self.user.id)

    def test_get_external_bank_with_admin_token(self):
        response = c.get(self.api_url, headers=c_header(self.admin_token))
        self.assertEqual(response.status_code, 200)
        data = response.json()['results']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[1]['name'], 'test2')

    def test_create_external_bank(self):
        response = c.post(self.api_url, {'name': 'test2', 'account_number': 'test2', 'information': 'test2'},
                          headers=c_header())
        self.assertEqual(response.status_code, 401)

    def test_create_external_bank_with_token(self):
        response = c.post(self.api_url, data={"name": "test2", 'account_number': 'te', 'information': 'test2'},
                          headers=c_header(self.token))
        self.assertEqual(response.status_code, 201, response.json())
        data = response.json()
        self.assertEqual(data['name'], 'test2')
        self.assertEqual(data['user'], self.user.id)

    def test_update_external_bank(self):
        response = c.put(f'{self.api_url}{self.external_bank.id}/',
                         {'name': 'test2', 'account_number': 'test2', 'information': 'test2'},
                         headers=c_header())
        self.assertEqual(response.status_code, 401)

    def test_update_external_bank_with_token(self):
        response = c.patch(f'{self.api_url}{self.external_bank.id}/',
                           {'name': 'test2', 'account_number': 'test2', 'information': 'test2'},
                           headers=c_header(self.token))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'test2')
        self.assertEqual(data['user'], self.user.id)

    def test_update_external_bank_of_another_user(self):
        response = c.patch(f'{self.api_url}{self.external_bank2.id}/',
                           {'name': 'test1', 'account_number': 'test2', 'information': 'test2'},
                           headers=c_header(self.token))
        self.assertEqual(response.status_code, 404)

    def test_update_external_bank_of_another_user_with_admin_token(self):
        response = c.patch(f'{self.api_url}{self.external_bank.id}/', {'name': 'test2'},
                           headers=c_header(self.admin_token))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'test2')
        self.assertEqual(data['user'], self.user.id)
