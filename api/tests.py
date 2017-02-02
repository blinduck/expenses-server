from django.test import TestCase, Client
from .models import *
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient


class BudgetTestCase(TestCase):
  fixtures = ['users.json', 'households.json', 'master_budgets.json']

  def test_budget_is_created_if_it_does_not_exist(self):
    assert len(Budget.objects.all()) == 0
    for mb in MasterBudget.objects.all():
      Budget.get_or_create_budget(mb)
    assert len(Budget.objects.all()) == 3

    for mb in MasterBudget.objects.all():
      Budget.get_or_create_budget(mb)
    assert len(Budget.objects.all()) == 3


class UserCreationTest(TestCase):
  def test_password_repeat_must_match_password(self):
    data = {
      'household': 'something',
      "username": "whee",
      "password": "password",
      "password_repeat": "different"}

    ser = UserSerializer(data=data)
    assert ser.is_valid() == False
    assert 'password' in ser.errors

  def test_creating_user(self):
    data = {
      'household': 'something',
      "username": "whee",
      "password": "password",
      "password_repeat": "password"}
    ser = UserSerializer(data=data)
    ser.is_valid()
    assert ser.is_valid()
    user = ser.save()
    assert user.username == 'whee'
    assert user.household.name == 'something'
    auser = authenticate(username='whee', password='password')
    assert user == auser


class SignUpTest(TestCase):
  def setUp(self):
    self.data = {
      'household': 'something',
      "username": "whee",
      "password": "password",
      "password_repeat": "password",
      'email': 'blinduck@gmail.com',
      'first_name': 'Deepan',
      'last_name': 'Bala'
    }
    self.client = APIClient()
    self.url = reverse('users_list')

  def test_signup(self):
    response = self.client.post(self.url, self.data, 'json')
    r_data = response.json()
    assert 'auth_token' in r_data
    assert r_data['auth_token']
    assert response.status_code == 201
    assert r_data['email'] == 'blinduck@gmail.com'

  def test_signup_with_existing_household_name(self):
    Household.objects.create(**{'name': self.data['household']})
    response = self.client.post(self.url, self.data, 'json')
    r_data = response.json()
    assert response.status_code == 400
    assert 'household' in r_data


class CreateMasterBudgetTest(TestCase):
  fixtures = [
    'users.json',
    'households.json',
  ]

  def setUp(self):
    self.client = APIClient()
    self.url = reverse('master_budget_list')
    self.deepan = User.objects.get(username='deepan')


  def test_create_masterbudget(self):

    data = {
      'name': 'testing budget',
      'amount': 200,
      'period': 'Monthly',
      'expense_type': 'Personal'
    }

    initial_budget_count = MasterBudget.objects.filter(user=self.deepan).count()
    assert initial_budget_count == 0
    self.client.force_authenticate(user=self.deepan)
    response = self.client.post(self.url, data, 'json')
    final_budget_count = MasterBudget.objects.filter(user=self.deepan).count()
    assert final_budget_count == 1

class CategoryTest(TestCase):
  fixtures = [
    'users.json',
    'households.json',
    'master_budgets.json',
    'category.json',
    'budget.json',
    'records.json'
  ]

  def setUp(self):
    self.client = APIClient()
    self.url = reverse('category_list')
    self.deepan = User.objects.get(username='deepan')
    self.client.force_authenticate(user=self.deepan)

  def test_getting_categories(self):
    self.client.force_authenticate(user=self.deepan)
    response = self.client.get(self.url)
    resp_data = response.json()
    assert resp_data['count'] == 2

  def test_creating_category(self):
    initial_cat_count = Category.objects.filter(
      household = self.deepan.household).count()
    resp = self.client.post(self.url, {'name': 'testing category'}, 'json')
    assert resp.status_code == 201
    final_cat_count = Category.objects.filter(
      household = self.deepan.household).count()
    print(initial_cat_count, final_cat_count)
    assert (initial_cat_count + 1) == final_cat_count




