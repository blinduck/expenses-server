from rest_framework.test import APIClient
from django.test import TestCase, Client
from .models import *
from .views import records_list
from django.core.urlresolvers import reverse


class RecordApiTestCase(TestCase):
  fixtures = [
    'users.json',
    'households.json',
    'master_budgets.json',
    'category.json',
    'budget.json',
    'records.json'
  ]

  def setUp(self):
    self.records_list_url = reverse('records_list')
    self.api_client = APIClient()
    self.julianne = User.objects.get(username='julianne')
    self.deepan = User.objects.get(username='deepan')


  def test_cannot_get_records_without_authenticated_user(self):
    c = Client()
    response = c.get(self.records_list_url)
    assert(response.status_code == 401)


  def test_can_get_some_records_if_authenticated(self):
    client = self.api_client
    client.force_authenticate(user=self.deepan)
    response = client.get(self.records_list_url)
    records = response.json()
    assert len(records) == 3
    client.force_authenticate(user=self.julianne)
    response = client.get(self.records_list_url)
    records = response.json()
    assert len(records) == 2

  def test_can_access_if_creator(self):
    client = self.api_client
    client.force_authenticate(user=self.julianne)
    record = Record.objects.filter(user=self.julianne).first()
    response = client.get(reverse('records_detail', kwargs={'pk': record.id}))
    assert response.status_code == 200
    assert int(response.json()['pk']) == record.pk

  def test_cannot_access_if_not_creator(self):
    client = self.api_client
    client.force_authenticate(user=self.deepan)
    record = Record.objects.filter(user=self.julianne).first()
    response = client.get(reverse('records_detail', kwargs={'pk': record.id}))
    print(response.status_code)
    print(response.content)
    # assert response.status_code == 401








